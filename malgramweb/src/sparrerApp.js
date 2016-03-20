var app = angular.module("sparrerApp", ['ngRoute', 'ngMaterial'])
	.config(function($mdThemingProvider, $mdIconProvider) {

		$mdIconProvider
			.defaultIconSet("./assets/img/menu.svg", 128)
			.icon("menu", "./assets/img/menu.svg", 32);

		$mdThemingProvider.theme('default')
			.primaryPalette('indigo');
	});
