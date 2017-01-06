'use strict';

registerDetailModule.component('registerDetail', {
  templateUrl: '/api/templates/register-detail.html',
  controller: function(
      $cookies,
      $http,
      $location,
      $routeParams,
      $scope
      ){
    var registerUrl = "/api/users/register/";
    $scope.registerError = {};
    $scope.user = {};
    var tokenExists = $cookies.get("token");
    if (tokenExists){
      // warn user
    };
    $scope.doRegister = function(user){

      if(user.email && user.email != user.email_check){
        $scope.registerError.password = ["Os endereços de email precisam ser iguais."];
      }
      var reqConfig = {
        method:"POST",
        url: registerUrl,
        data : {
          username: user.username,
          email: user.email,
          email_check: user.email_check,
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
        console.log(e_data) // error
        $scope.registerError = e_data
      });
    };
  },
});
