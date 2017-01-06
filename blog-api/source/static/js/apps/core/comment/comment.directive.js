'use strict';

commentModule.directive('commentReplyThread', function(Comment, $cookies){
  return {
    restrict: "E",
    scope: {
      comment: "=comment",
      slug: "=slug",
    },
    template: `
      <ul>
        <li ng-repeat="reply in replies">
          {{reply.content}}
          <br/>
          por {{ reply.user.username }} | 
          <a 
            href="#"
            confirm-click="Tem certeza?"
            confirmed-click="deleteComment(reply)"
            ng-show="reply.user.username == currentUser">
            Remover
          </a>
          <hr/>
        </li>
      </ul>
      <div ng-hide="replies">
        <i class="fa fa-spinner fa-pulse fa-2x fa-fw"></i>
        <span class="sr-only">Carregando...</span>
      </div>
      <p style="color: red;" ng-if="reply.content" >PREVIEW: {{reply.content}}</p>
      <form ng-submit="addCommentReply(reply, comment)">
        <div class="form-group" ng-class"{{ "has-error": replyError.content }}">
          <textarea id="replyText-{{ reply.id }}" class="form-control" ng-model="reply.content"></textarea>
          <label class="control-label" for="replyText-{{ reply.id}}" ng-if="replyError"><span ng-repeat="error in replyError.content">{{ content.error }}"</span></label>
        </div>
        <input class="btn btn-default" type="submit">
      </form>`,
    link: function(scope, element, attr){
      if($cookies.get('token')){
        scope.currentUser = $cookies.get('username')
      }
      if (scope.comment){
        var commentId = scope.comment.id
        if (commentId){
          Comment.get(
            { id: commentId },
            function(data){
              scope.replies = data.replies
            }
          );
        }
      }
      scope.addCommentReply = function(reply, parentComment){
        Comment.create(
            {
            content: reply.content,
            slug: scope.slug,
            type: 'post',
            parent_id: parentComment.id
          },
          function(data){
            //success
            console.log(data);
            scope.comments.replies.push(data);
            parentComment.reply_count += 1;
            reply.content = "";
            //resetReply();
          },
          function(e_data){
            //error
            //console.log(e_data);
          }
        )
      }
      scope.deleteCommentReply = function(reply, parentComment){
        Comment.delete(
          { id: reply.id },
          function(data){
            var index = scope.replies.indexOf(comment);
            scope.replies.splice(comment, 1)
          },
          function(e_data){
            //console.log(e_data)
          }
        );

      }
    }
  };
});
