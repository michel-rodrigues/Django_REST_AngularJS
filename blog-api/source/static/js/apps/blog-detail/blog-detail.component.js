'use strict';

blogDetailModule.component('blogDetail', {
  templateUrl: '/api/templates/blog-detail.html',
  controller: function(Comment, Post, $cookies, $http, $location, $routeParams, $scope){
    
    var slug = $routeParams.slug

    $scope.commentOrder = '-timestamp';

    Post.get({"slug": slug}, function(data){
      $scope.post = data;
      Comment.query({"slug": slug, "type": "post"}, function(data){
        $scope.comment = data;
      });
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
      Comment.delete(
          {id: comment.id},
          function(data){
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
