"""yara test settings

Revision ID: 8d1a65d94f4b
Revises: b67c53c89680
Create Date: 2018-09-29 13:49:15.428509

"""

from app.models import cfg_settings
from alembic import op
import datetime

# revision identifiers, used by Alembic.
revision = '8d1a65d94f4b'
down_revision = 'b67c53c89680'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    date_created = datetime.datetime.now().isoformat()
    date_modified = datetime.datetime.now().isoformat()

    op.bulk_insert(
        cfg_settings.Cfg_settings.__table__,
        [
            {"key": "SIGNATURE_TESTING_COMMAND", "value": '/usr/bin/yara RULE FILE_PATH',
             "public": True,
             "date_created": date_created,
             "description": "Command to run when testing signatures. RULE will be replaced by the current rule being tested and FILE_PATH with attached files.",
             "date_modified": date_modified},
            {"key": "SIGNATURE_TESTING_COMMAND_SUCCESS_REGEX", "value": '[A-Za-z0-9]',
             "public": True,
             "date_created": date_created,
             "description": "When testing signatures, if stdout matches against this regex, the test is marked successful. If it isn't, it is marked unsuccessful.",
             "date_modified": date_modified}

        ]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    keys = ["SIGNATURE_TESTING_COMMAND", "SIGNATURE_TESTING_COMMAND_SUCCESS_REGEX"]
    for key in keys:
        op.execute("""DELETE from cfg_settings where `key`='%s';""" % (key))
        # ### end Alembic commands ###
