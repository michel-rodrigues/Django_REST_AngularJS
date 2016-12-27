'use strict';

blogDetailModule.component('blogDetail', {
  templateUrl: '/api/templates/blog-detail.html',
  controller: function(Post, $cookies, $http, $location, $routeParams, $scope){

    // $scope.notFound = true;
    
    var slug = $routeParams.slug

    Post.get({"slug": slug}, function(data){
      $scope.post = data;
      console.log(data);
      $scope.comments = data.comments; // linha inútil do tutorial
    });

    //Post.query(function(data){
    //  angular.forEach(data, function(post){
    //    if (post.id == $routeParams.id){
    //      // $scope.notFound = false;
    //      $scope.post = post;
    //      resetReply();
    //    }
    //  });
    //});

    $scope.deleteComment = function(comment){
      $scope.$apply(
        $scope.post.comments.splice(comment, 1)
      );
      // someResource.$delete() //API
    };

    // Authorization: JWT {"content":"my new reply to another try"} http://127.0.0.1:8000/api/comments/create/?slug=new-title&type=post&parent_id=13'

    $scope.addReply = function(){
        var token = $cookies.get("token")
        if (token){
          var req = {
            url: "/api/comments/create/",
            method: "POST",
            data: {
              content: $scope.reply.content,
              slug: slug,
              type: 'post'
            },
            headers: {
              authorization: "JWT " + token
            }
          };
          var requestAction = $http(req);
          requestAction.success(function(r_data, r_status, r_headers, r_config){
            $scope.post.comments.push($scope.reply);
            resetReply();
          });
          requestAction.error(function(e_data, e_status, e_headers, e_config){
            console.log(e_data);
          });
        }
        else {
          console.log("NO TOKEN");
        }
    }

    function resetReply(){
      $scope.reply = {
        id: $scope.post.comments.length + 1,
        content: ""
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
