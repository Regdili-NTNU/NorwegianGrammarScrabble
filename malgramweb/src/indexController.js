app.controller("indexController", function($scope, translationService, pointService) {
	$scope.ts = translationService;

	$scope.pointService = pointService;
	$scope.pointService.score = undefined;
});
