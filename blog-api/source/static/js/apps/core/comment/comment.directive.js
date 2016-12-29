'use strict';

commentModule.directive('commentReplyThread', function(Comment){
  return {
    restrict: "E",
    scope: {
      comment: "=comment",
    },
    template: `
      <ul><li ng-repeat="reply in replies">{{reply.content}}</li></ul>
      <div ng-hide="replies">
        <i class="fa fa-spinner fa-pulse fa-2x fa-fw"></i>
        <span class="sr-only">Loading...</span>
      </div>
      `,
    link: function(scope, element, attr){
      var commentId = scope.comment.id
      if (scope.comment){
        if (commentId){
          Comment.get(
            {id: commentId},
            function(data){
              scope.replies = data.replies
            }
          );
        }
      }
    }
  };
});


