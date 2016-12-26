'use strict';

tryNavModule.directive('tryNav', function(Post, $location){
  return {
    restrict: "E",
    templateUrl: "/templates/nav.html",
    link: function(scope, element, attr){
      scope.items = Post.query();
      scope.selectItem = function($item, $model, $label){
        // console.log($item); // resource
        // console.log($model);
        // console.log($label);
        $location.path("/blog/" + $item.id);
        scope.searchQuery = "";
      };
      scope.searchItem = function(){
        $location.path("/blog/").search("q", scope.searchQuery);
        scope.searchQuery = "";
      };
    },
  };
});


