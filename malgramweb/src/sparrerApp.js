angular.module("angular-json-rpc",[]).config(["$provide",function(a){return a.decorator("$http",["$delegate",function(a){return a.jsonrpc=function(b,c,d,e){var f={jsonrpc:"2.0",method:c,params:d,id:1};return a.post(b,f,angular.extend({headers:{"Content-Type":"application/json"}},e))},a}])}]);

var app = angular.module("sparrerApp", ['ngMaterial', 'ngMdIcons', 'angular-json-rpc'])
	.config(function($mdThemingProvider, $mdIconProvider) {

		$mdIconProvider
			.defaultIconSet("./assets/img/menu.svg", 128)
			.icon("menu", "./assets/img/menu.svg", 32);

		$mdThemingProvider.theme('default')
			.primaryPalette('indigo');
	});
