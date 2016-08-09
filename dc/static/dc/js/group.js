Sortable.create(source_group, {
    group: "grouping",
    animation: 100
});

[].forEach.call(destination_group.getElementsByClassName('block__list'), function(e) {
    Sortable.create(e, {
        group: "grouping",
        animation: 0,
        sort: false,
    });
});

var app = angular.module( "groupingApp", [] ).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller(
    "groupingController", [ '$scope', '$http', '$log', '$location', '$window',
    function( $scope, $http, $log, $location, $window ) {
        $scope.numGroups = 2;

        $scope.addGroup = function() {
            var groups = document.getElementById("destination_group");

            var newGroup = document.createElement("div");
            newGroup.id = "group-" + $scope.numGroups++;
            newGroup.className = "layer"

            var groupTitle = document.createElement("div");
            groupTitle.className = "layer title";
//            groupTitle.innerHTML = "Group " + $scope.numGroups;
            groupTitle.innerHTML = `<input type="text" value="Group ${$scope.numGroups}" id="group-${$scope.numGroups}_title">`

            newGroup.appendChild(groupTitle);

            var groupEl = document.createElement("ul");
            groupEl.className = "block__list block__list_tags";
            newGroup.appendChild(groupEl);

            groups.appendChild(newGroup);

            Sortable.create(groupEl,
            {
                group: 'grouping',
                animation: 100,
                ghostClass: '.sortable-ghost'
            }
            );
        }

        $scope.saveOrdering = function() {
            var source_group = document.getElementById("source_group");
            if( source_group.getElementsByTagName('li').length > 0) {
                alert("Please sort all statements");
                return false;
            }

            var groups = document.getElementById("destination_group");
            var o = [];

            var submit = true;

            [].every.call(groups.children, function(group) {
                var g = [];

                let group_name = group.getElementsByTagName('input')[0].value;
                [].forEach.call(group.getElementsByTagName('li'), function(element) {
                    g.push({ 'name': element.innerHTML, 'id': element.id, 'group_name': group_name});
                });

                if(g.length == 0) {
                    groups.removeChild(group);
                } else
                if(g.length < 2) {
                    alert("Please make sure each group has at least two items.");
                    submit = false;
                    return false;
                } else {
                    o.push(g);
                }

                return true;
            });

            if(submit) {
                if(confirm("Have you checked that all statements have been classified in the way that makes most sense to you?")) {
                    $http(
                        { 'method': 'POST',
                        'url': '/group/',
                        'data': o
                        }
                    ).
                    success(function(data, status, headers, config) {
                        $window.location.href = '/rate/';
                        $window.location.href;
                    });
                } else {
                    return false;
                }
            } else {
                return false;
            }
        };
    }
]);
