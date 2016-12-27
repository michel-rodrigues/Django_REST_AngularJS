'use strict';

//angular.module('blogList')
blogListModule.component('blogList', {
  templateUrl: '/api/templates/blog-list.html',
  controller: function(Post, $cookies, $location, $rootScope, $scope){

    var q = $location.search().q;

    if(q){
      $scope.query = q;
      $scope.searchQuery = true;
    }

    $scope.order = "-publishDate";

    $scope.goToItem = function(item){
      //$rootScope.$apply(function(){
        // console.log(item);
        $location.path("/blog/" + item.id);
      //});
    };

    Post.query(
      function(data){
        $scope.items = data;
        setupCol(3);
      },
      function(errorData){
        
      }
    );

    function setupCol(number){
      if (angular.isNumber(number)){
        $scope.numCols = number // Usar múltiplos de 12
      }
      else {
        $scope.numCols = 3 // Usar múltiplos de 12
      }
      $scope.cssClass = 'col-sm-' + (12 / $scope.numCols)
    };

    $scope.loadingQuery = false
    $scope.$watch(function(){
      if($scope.query) {
        $scope.loadingQuery = true
        $scope.cssClass = 'col-sm-3'
        if($scope.query != q){
          $scope.searchQuery = false;
        }
      }
      else {
        if ($scope.loadingQuery) {
          setupCol(3)
          $scope.loadingQuery = false
        }
      }
    })



    // Post.query(
    //   function(data){
    //     setupCol(data, 3);
    //   },
    //   function(errorData){
    //     
    //   }
    // );

    // $scope.loadingQuery = false
    // $scope.$watch(function(){
    //   if($scope.query) {
    //     $scope.loadingQuery = true
    //     $scope.cssClass = 'col-sm-12'
    //   }
    //   else {
    //     if ($scope.loadingQuery) {
    //       setupCol($scope.items, 3)
    //       $scope.loadingQuery = false
    //     }
    //   }
    // })

    // // $scope.chanceCols = function(number){
    // //   if (angular.isNumber(number)){
    // //     $scope.numCols = number // Usar múltiplos de 12
    // //   }
    // //   else {
    // //     $scope.numCols = 3 // Usar múltiplos de 12
    // //   }
    // //   setupCol(data, $scope.numCols)      
    // // }

    // function setupCol(data, number){
    //   $scope.items = data
    //   if (angular.isNumber(number)){
    //     $scope.numCols = number // Usar múltiplos de 12
    //   }
    //   else {
    //     $scope.numCols = 3 // Usar múltiplos de 12
    //   }
    //   $scope.cssClass = 'col-sm-' + (12 / $scope.numCols)
    //   $scope.colItems = chunkArrayInGroups($scope.items, $scope.numCols)
    // };

    // // Cria um array de arrays
    // function chunkArrayInGroups(array, unit) {
    //   var results = [];
    //   var len = Math.ceil(array.length / unit);
    //   for (var i = 0; i < len; i++) {
    //     results.push(array.slice(i * unit, (i + 1) * unit));
    //   }
    //   return results;
    // }

  },
});
