'use strict';

angular.module('InquestKB')
    .controller('C2dnsController', ['$scope', '$modal', 'resolvedC2dns', 'C2dns', 'Cfg_states',
        function ($scope, $modal, resolvedC2dns, C2dns, Cfg_states) {

            $scope.c2dns = resolvedC2dns;

            $scope.create = function () {
                $scope.clear();
                $scope.open();
            };

            $scope.update = function (id) {
                $scope.c2dns = C2dns.get({id: id});
                $scope.cfg_states = Cfg_states.query();
                $scope.open(id);
            };

            $scope.delete = function (id) {
                C2dns.delete({id: id},
                    function () {
                        $scope.c2dns = C2dns.query();
                    });
            };

            $scope.save = function (id) {
                if (id) {
                    C2dns.update({id: id}, $scope.c2dns,
                        function () {
                            $scope.c2dns = C2dns.query();
                            //$scope.clear();
                        });
                } else {
                    C2dns.save($scope.c2dns,
                        function () {
                            $scope.c2dns = C2dns.query();
                            //$scope.clear();
                        });
                }
            };

            $scope.clear = function () {
                $scope.c2dns = {

                    "date_created": "",

                    "date_modified": "",

                    "state": "",

                    "domain_name": "",

                    "match_type": "",

                    "reference_link": "",

                    "reference_text": "",

                    "expiration_type": "",

                    "expiration_timestamp": "",

                    "id": ""
                };
            };

            $scope.open = function (id) {
                var c2dnsSave = $modal.open({
                    templateUrl: 'c2dns-save.html',
                    controller: 'C2dnsSaveController',
                    resolve: {
                        c2dns: function () {
                            return $scope.c2dns;
                        }
                    }
                });

                c2dnsSave.result.then(function (entity) {
                    $scope.c2dns = entity;
                    $scope.save(id);
                });
            };
        }])
    .controller('C2dnsSaveController', ['$scope', '$modalInstance', 'c2dns', 'Cfg_states', 'Comments',
        function ($scope, $modalInstance, c2dns, Cfg_states, Comments) {
            $scope.c2dns = c2dns;
            $scope.c2dns.new_comment = "";
            $scope.Comments = Comments;

            $scope.cfg_states = Cfg_states.query();

            $scope.add_comment = function (id) {
                $scope.Comments.resource.save({
                    comment: $scope.c2dns.new_comment,
                    entity_type: Comments.ENTITY_MAPPING.DNS,
                    entity_id: id
                }, function () {
                    $scope.c2dns.new_comment = "";
                    $scope.c2dns.comments = $scope.Comments.resource.query({
                        entity_type: Comments.ENTITY_MAPPING.DNS,
                        entity_id: id
                    })
                });
            };

            $scope.ok = function () {
                $modalInstance.close($scope.c2dns);
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };
        }]);
