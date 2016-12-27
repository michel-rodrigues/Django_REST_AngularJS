'use strict';

loginDetailModule.component('loginDetail', {
  templateUrl: '/api/templates/login-detail.html',
  controller: function(
      $cookies,
      $http,
      $location,
      $routeParams,
      $scope
      ){
    var loginUrl = "/api/auth/token/";
    $scope.user = {
    
    };
    var tokenExists = $cookies.get("token");
    if (tokenExists){
      $scope.loggedIn = true;
      $cookies.remove("token");
      $scope.user = {
        username: $cookies.get("username"),
      };
    };
    $scope.doLogin = function(user){
      console.log(user);
      var reqConfig = {
        method:"POST",
        url: loginUrl,
        data : {
          username: user.username,
          password: user.password
        },
        headers: {}
      };
      var requestAction = $http(reqConfig);
      requestAction.success(function(r_data, r_status, r_headers, r_config){
        console.log(r_data); // token
        $cookies.put("token", r_data.token);
        $cookies.put("username", user.username);
        $location.path("/");
      });
      requestAction.error(function(e_data, e_status, e_headers, e_config){
        console.log(e_data.non_field_errors[0]) // error
        console.log(e_data) // error
      });
    };
  },
});
