Sortable.create(source_group, {
    group: "grouping",
    animation: 100
});

[].forEach.call(destination_group.getElementsByClassName('block__list'), function(e) {
    Sortable.create(e, {
        group: "grouping",
        animation: 100
    });
});

var app = angular.module( "groupingApp", [] ).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller(
    "groupingController", [ '$scope', '$http', '$log', '$location',
    function( $scope, $http, $log, $location ) {
        $scope.numGroups = 2;

        $scope.addGroup = function() {
            var groups = document.getElementById("destination_group");

            var newGroup = document.createElement("div");
            newGroup.id = "group-" + $scope.numGroups++;

            newGroup.className = "layer col-md-2"

            var groupTitle = document.createElement("div");
            groupTitle.innerHTML = "Group";
            groupTitle.className = "layer title";
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
                return;
            }

            var groups = document.getElementById("destination_group");
            var o = [];

           [].every.call(groups.children, function(group) {
                var g = [];
                [].forEach.call(group.getElementsByTagName('li'), function(element) {
                    g.push({ 'name': element.innerHTML, 'id': element.id});
                })

                if(g.length == 0) {
                    groups.removeChild(group);
                } else
                if(g.length < 2) {
                    alert("Please make sure each group has at least two items.");
                    return false;
                } else {
                    o.push(g);
                }
                return true;
            });

            $http(
            { 'method': 'POST',
              'url': '/group/',
              'data': o
            }
            ).
            success(function(data, status, headers, config) {
                $location.path(config.url)
            });
        };
    }
]);
