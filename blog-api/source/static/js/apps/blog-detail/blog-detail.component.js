'use strict';

blogDetailModule.component('blogDetail', {
  templateUrl: '/api/templates/blog-detail.html',
  controller: function(Post, $http, $location, $routeParams, $scope){

    // $scope.notFound = true;

    Post.query(function(data){
      angular.forEach(data, function(post){
        if (post.id == $routeParams.id){
          // $scope.notFound = false;
          $scope.post = post;
          resetReply();
        }
      });
    });

    $scope.deleteComment = function(comment){
      $scope.$apply(
        $scope.post.comments.splice(comment, 1)
      );
      // someResource.$delete() //API
    };

    $scope.addReply = function(){
      $scope.post.comments.push($scope.reply);
      resetReply();
    }

    function resetReply(){
      $scope.reply = {
        "id": $scope.post.comments.length + 1,
        "text": ""
      };
    };

    //if ($scope.notFound){
    //  $location.path("/404");
    //};

    // $http.get("/json/posts.json").then(successCallback, errorCallback);

    // function successCallback(response, status, config, statusText){
    //   $scope.notFound = true;

    //   var blogItems = response.data

    //   angular.forEach(blogItems, function(post){
    //     if (post.id == $routeParams.id){
    //       $scope.notFound = false;
    //       $scope.post = post;
    //     }
    //   });
    // };
    // 
    // function errorCallback(response, status, config, statusText){
    //   $scope.notFound = true;
    //   console.log(response)
    // };


    // if ($scope.notFound){
    //   $location.path("/404");
    // };



    //console.log($routeParams);
    //var blogItems = [
    //  {'title': 'Título 1', 'id': 1, 'description': 'This is the post 1'},
    //  {'title': 'Título 2', 'id': 2, 'description': 'This is the post 2'},
    //  {'title': 'Título 3', 'id': 3, 'description': 'This is the post 3'},
    //  {'title': 'Título 4', 'id': 4, 'description': 'This is the post 4'},
    //  {'title': 'Título 5', 'id': 5, 'description': 'This is the post 5'},
    //];

    ////$scope.title =  "Blog " +  $routeParams.id;
    //$scope.notFound = true;
    //angular.forEach(blogItems, function(post){
    //  if (post.id == $routeParams.id){
    //    $scope.notFound = false;
    //    $scope.post = post;
    //  }
    //});


    //$scope.title =  "Blog " +  $routeParams.id;

    //angular.forEach(blogItems, function(blog){
    //  if (blog.id == $routeParams.id){
    //    $scope.title = blog.title;
    //    $scope.description = blog.description;
    //  }
    //});

  },
});
