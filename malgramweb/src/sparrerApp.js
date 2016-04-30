var app = angular.module("sparrerApp", ['ngRoute', 'ngMaterial'])
	.config(function($mdThemingProvider, $mdIconProvider, $routeProvider) {

		$mdIconProvider
			.defaultIconSet("./assets/img/menu.svg", 128)
			.icon("menu", "./assets/img/menu.svg", 32);

		$mdThemingProvider.theme('default')
			.primaryPalette('indigo');

		$routeProvider.when('/play/:language?', {
			templateUrl: 'play.html',
			controller: 'playController'
		}).when('/start', {
			templateUrl: 'start.html',
			controller: 'startController'
		}).otherwise({
			redirectTo: '/start'
		});
	});
