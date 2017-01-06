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
    var loginUrl = "/api/users/login/";
    $scope.loginError = {};
    $scope.user = {};
    var tokenExists = $cookies.get("token");
    if (tokenExists){
      $scope.loggedIn = true;
      $cookies.remove("token");
      $scope.user = {
        username: $cookies.get("username"),
      };
      window.location.reload()
    };
    $scope.doLogin = function(user){
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
        $cookies.put("username", r_data.username);
        $location.path("/");
        //window.location.reload()
      });
      requestAction.error(function(e_data, e_status, e_headers, e_config){
        console.log(e_data.detail) // error
        $scope.loginError = e_data
      });
    };
  },
});
