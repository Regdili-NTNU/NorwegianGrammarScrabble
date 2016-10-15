app.controller("startController", function($scope, $http, $mdDialog, translationService) {
	$scope.alltime_scores = [];
	$scope.weekly_scores = [];
	$scope.ts = translationService;
	$scope.ts.setLanguage(undefined);

	$scope.getWeeklyScores = function() {
			$http.post('http://regdili.hf.ntnu.no:5051/server/get_weekly_scores').then(
				function(result) {
					let data = JSON.parse(result.data);
					$scope.weekly_scores = data["scores"];
				}, function() {
				});
		};

	$scope.getHighScores = function() {
			$http.post('http://regdili.hf.ntnu.no:5051/server/get_high_scores').then(
				function(result) {
					let data = JSON.parse(result.data);
					$scope.alltime_scores = data["scores"];
				}, function() {
				});
		};


	$scope.getHighScores();
	$scope.getWeeklyScores();
});
