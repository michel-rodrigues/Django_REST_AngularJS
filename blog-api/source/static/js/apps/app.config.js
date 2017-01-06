'use strict';

app.config(function($locationProvider, $resourceProvider, $routeProvider){

    $locationProvider.html5Mode({enabled:true}),

    $resourceProvider.defaults.stripTrailingSlashes = false;

    $routeProvider
      .when("/", {
        template: "<blog-list></blog-list>"
      })
      .when("/about", {
        templateUrl: "/app/templates/about.html"
      })
      .when("/blog", {
        template: "<blog-list></blog-list>"
      })
      .when("/blog/:slug", {
        template: "<blog-detail></blog-detail>"
      })
      .when("/register", {
        template: "<register-detail></register-detail>"
      })
      .when("/login", {
        template: "<login-detail></login-detail>"
      })
      .when("/logout", {
        //template: "<login-detail></login-detail>"
        redirectTo: "/login"
      })
      .otherwise({
        template: "<h1>Opss... Not Found - Error 404</h1>"
      })
  });
