'use strict';

interceptorModule.factory('LoginRequiredInterceptor', function($cookies, $location){
  return function(response){
    if(response.status == 401 || response.status == 403){
      var currentPath = $location.path();
      console.log(currentPath);
      if(currentPath == "/login"){
        $location.path("/login")
      }
      else {
        $location.path("/login").search("next", currentPath);
      }
    }
  }
});
