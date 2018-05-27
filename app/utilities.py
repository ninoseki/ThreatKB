import re
import json
import sys

from plyara import Plyara

from more_itertools import unique_everseen
from app.models import cfg_settings

from app.models.c2dns import C2dns
from app.models.c2ip import C2ip
from app.models.yara_rule import Yara_rule

# Appears that Ply needs to read the source, so disable bytecode.
sys.dont_write_bytecode


#####################################################################

def extract_ips_text(text):
    regex = cfg_settings.Cfg_settings.get_setting(key="IMPORT_IP_REGEX")
    ip_regex = regex if regex else '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:\/\d{1,3})?)'
    return re.compile(ip_regex).findall(text)


#####################################################################

def extract_dns_text(text):
    hostnames = []
    regex = cfg_settings.Cfg_settings.get_setting(key="IMPORT_DNS_REGEX")
    url_regex = regex if regex else 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    for dns in re.compile(url_regex).findall(text):
        try:
            hostnames.append(dns)
        except:
            pass
    return hostnames


#####################################################################

def extract_yara_rules_text(text):
    split_regex = cfg_settings.Cfg_settings.get_setting(key="IMPORT_SIG_SPLIT_REGEX")
    split_regex = split_regex if split_regex else "\n[\t\s]*\}[\s\t]*(rule[\t\s][^\r\n]+(?:\{|[\r\n][\r\n\s\t]*\{))"
    parse_regex = cfg_settings.Cfg_settings.get_setting(key="IMPORT_SIG_PARSE_REGEX")
    parse_regex = parse_regex if parse_regex else r"^[\t\s]*rule[\t\s][^\r\n]+(?:\{|[\r\n][\r\n\s\t]*\{).*?condition:.*?\r?\n?[\t\s]*\}[\s\t]*(?:$|\r?\n)"

    yara_rules = re.sub(split_regex, "}\r?\n\\1", text, re.MULTILINE | re.DOTALL)
    yara_rules = re.compile(parse_regex, re.MULTILINE | re.DOTALL).findall(yara_rules)
    extracted = []
    for yara_rule_original in yara_rules:
        try:
            parsed_rule = parse_yara_rules_text(yara_rule_original)[0]

            strings, condition = get_strings_and_conditions(yara_rule_original)
            extracted.append({"parsed_rule": parsed_rule, "strings": strings, "condition": condition})
        except Exception, e:
            pass

    return extracted


#####################################################################

def get_strings_and_conditions(rule):
    segment_headers = \
        {
            "strings": "^\s*strings:\s*\r?\n?",
            "condition": "^\s*condition:\s*\r?\n?",
        }
    segments = \
        {
            "strings": [],
            "condition": [],
        }
    SEGMENT = None
    for line in rule.splitlines():
        segment_change = False
        for header, rx in segment_headers.items():
            if re.match(rx, line):
                SEGMENT = header
                segment_change = True
        if SEGMENT and not segment_change:
            segments[SEGMENT].append(line)

    segments["strings"][-1] = segments["strings"][-1].rstrip(" }") if not "=" in segments["strings"][-1] else \
    segments["strings"][-1]
    segments["condition"][-1] = segments["condition"][-1].rstrip(" }")
    return "\n".join(segments["strings"]), "\n".join(segments["condition"])

#####################################################################

def extract_artifacts_by_type(type_, import_objects):
    table_mapping = {"ip": C2ip, "domain_name": C2dns}
    output = []
    processed = set()

    for import_object in import_objects:
        if import_object[type_] in processed:
            continue

        processed.add(import_object[type_])
        temp_object = {"type": type_, "metadata": {}, "artifact": import_object[type_]}
        for key, val in import_object.iteritems():
            if key.lower() == type_ or key.lower() == "artifact":
                continue
            elif key in table_mapping[type_].__table__.columns.keys():
                temp_object[key] = val
            else:
                temp_object["metadata"][key] = val

        output.append(temp_object)

    return output


#####################################################################

def extract_artifacts_json(do_extract_ip, do_extract_dns, do_extract_signature, import_objects):
    ips = extract_artifacts_by_type("ip", [import_object for import_object in import_objects if "ip" in import_object])
    dns = extract_artifacts_by_type("domain_name", [import_object for import_object in import_objects if
                                                    "domain_name" in import_object])
    temp = []
    output = []

    if do_extract_ip:
        output.extend(ips)
    if do_extract_dns:
        output.extend(dns)

    return output


#####################################################################

def extract_artifacts_text(do_extract_ip, do_extract_dns, do_extract_signature, text):
    ips = extract_ips_text(text)
    dns = extract_dns_text(text)
    yara_rules = extract_yara_rules_text(text)
    temp = []
    output = []

    if do_extract_ip:
        output.extend([{"type": "IP", "artifact": ip} for ip in list(unique_everseen(ips))])
    if do_extract_dns:
        output.extend([{"type": "DNS", "artifact": hostname} for hostname in list(unique_everseen(dns))])
    if do_extract_signature:
        for yara_rule in yara_rules:
            yr = yara_rule["parsed_rule"]  # hacky
            if not yr["rule_name"] in temp:
                temp.append(yr["rule_name"])
                output.append(
                    {"type": "YARA_RULE", "artifact": yr["rule_name"], "rule": yr, "strings": yara_rule["strings"],
                     "condition": yara_rule["condition"]})

    return output


#####################################################################

def extract_artifacts(do_extract_ip, do_extract_dns, do_extract_signature, text):
    try:
        import_objects = json.loads(str(text).encode("string_escape"))
        return extract_artifacts_json(do_extract_ip, do_extract_dns, do_extract_signature, import_objects)
    except ValueError, e:
        return extract_artifacts_text(do_extract_ip, do_extract_dns, do_extract_signature, text)

    return output


#####################################################################

def parse_yara_rules_file(filename):
    return parse_yara_rules_text(open(filename, "r").read())

#####################################################################

def parse_yara_rules_text(text):
    return Plyara().parse_string(text)
