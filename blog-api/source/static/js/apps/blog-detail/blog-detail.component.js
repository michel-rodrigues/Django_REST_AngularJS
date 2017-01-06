'use strict';

blogDetailModule.component('blogDetail', {
  // templateUrl: '/api/templates/blog-detail.html',
  template: '<ng-include src="getTemplateUrl()">',
  controller: function(Comment, Post, $cookies, $http, $location, $routeParams, $scope){
    $scope.loading = true;
    $scope.post = null;
    $scope.pageError = false;
    $scope.notFound = false;
    $scope.getTemplateUrl = function(){
      if($scope.loading && $scope.post == null){
        return '/api/templates/utils/loading-detail.html';
      }
      else if ($scope.notFound){
        return '/api/templates/utils/not-found.html';
      }
      else if ($scope.pageError){
        return '/api/templates/utils/page-error.html';
      }
      else{
        return '/api/templates/blog-detail.html';
      }
    };

    if($cookies.get('token')){
      $scope.currentUser = $cookies.get('username')
    }

    function postDataSuccess(data){
      $scope.loading = false;
      $scope.post = data;
      Comment.query({"slug": slug, "type": "post"}, function(data){
        $scope.comment = data;
      }); 
    };

    function postDataError(e_data){
      $scope.loading = false;
      if(e_data.status == 404){
        $scope.notFound = true;
      }
      else {
        $scope.pageError = true;
      }
    };

    var slug = $routeParams.slug

    $scope.commentOrder = '-timestamp';

    Post.get({"slug": slug}, postDataSuccess, postDataError);

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
      Comment.delete(
          { id: comment.id },
          function(data){
            var index = $scope.post.comments.indexOf(comment);
            $scope.post.comments.splice(comment, 1)
          },
          function(e_data){
            //console.log(e_data)
          }
      );

      //$scope.$apply(
      //  $scope.post.comments.splice(comment, 1)
      //);
    };
    $scope.updateReply = function(comment){
      Comment.update(
        {
          id: comment.id,
          content: $scope.reply.content,
          slug: slug,
          type: 'post'
        },
        function(data){
          //success
          console.log(data);
          //$scope.comments.push(data);
          resetReply();
        },
        function(e_data){
          //error
          //console.log(e_data);
        }
      );
    }
    $scope.reply = {};
    $scope.addCommentReply = function(reply, parentComment){
      console.log(reply);
      console.log(parentComment)
      Comment.create(
          {
          content: reply.content,
          slug: slug,
          type: 'post',
          parent_id: parentComment.id
        },
        function(data){
          //success
          console.log(data);
          //$scope.comments.push(data);
          parentComment.reply_count += 1;
          reply.content = "";
          //resetReply();
        },
        function(e_data){
          //error
          //console.log(e_data);
          scope.replyError = e_data.data;
        }
      )
    }
    $scope.addNewComment = function(){
      Comment.create(
        {
          content: $scope.newComment.content,
          slug: slug,
          type: 'post'
        },
        function(data){
          //success
          console.log(data);
          $scope.comments.push(data);
          resetReply();
          $scope.commentError = '';
        },
        function(e_data){
          //error
          //console.log(e_data);
          $scope.commentError = e_data.data;
        }
      );
    }
    function resetReply(){
      $scope.reply = {
        //id: $scope.post.comments.length + 1,
        content: ""
      };
    };
  },
});
