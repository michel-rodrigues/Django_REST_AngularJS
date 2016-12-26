'use strict';

app.config(function($locationProvider, $routeProvider){
    
    $locationProvider.html5Mode({enabled:true}),

    $routeProvider
      .when("/", {
        template: "<blog-list></blog-list>"
      })
      .when("/about", {
        templateUrl: "/templates/about.html"
      })
      .when("/blog", {
        template: "<blog-list></blog-list>"
      })
      .when("/blog/:id", {
        template: "<blog-detail></blog-detail>"
      })
      .otherwise({
        template: "<h1>Opss... Not Found - Error 404</h1>"
      })
  });
