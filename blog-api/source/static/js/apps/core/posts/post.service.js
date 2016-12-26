'use strict';

postModule.factory('Post', function($resource){
  var url = "/static/json/posts.json"
  return $resource(url, {}, {
    query:{
      method: "GET",
      params: {},
      isArray: true, // default
      cache: true,
    },
    get:{
      method: "GET",
      // params: {"id": @id},
      isArray: true, // false
      cache: true,
    },
  })
});
