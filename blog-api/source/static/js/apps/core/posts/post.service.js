'use strict';

postModule.factory('Post', function($resource){
  var url = "/api/posts/:slug/"
  return $resource(url, {}, {
    query:{
      method: "GET",
      params: {},
      isArray: true, // default
      cache: false,
      transformResponse: function(data, headersGetter, status){
        var finalData = angular.fromJson(data);
        // console.log(finalData.results);
        return finalData.results;
      }
    },
    get:{
      method: "GET",
      params: {slug: "@slug"},
      isArray: false,
      cache: false,
    },
  })
});
