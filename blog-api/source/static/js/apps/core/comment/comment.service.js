'use strict';

postModule.factory('Comment', function($resource){
  var url = "/api/comments/";
  var commentQuery = {
    url: url,
    method: "GET",
    params: {},
    isArray: true,
    cache: false,
    transformResponse: function(data, headersGetter, status){
      var finalData = angular.fromJson(data);
      // console.log(finalData.results);
      return finalData.results;
    }
  };
  var commentGet = {
    url: url + ":id/",
    method: "GET",
    params: {id: "@id"},
    isArray: false,
    cache: false,
  };

  return $resource(url, {}, {
    query: commentQuery,
    get: commentGet
  })
});
