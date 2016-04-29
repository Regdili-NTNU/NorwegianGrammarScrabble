app.controller("scoresController", function($scope, $http, $mdDialog) {
	$scope.scores = [];

	$scope.getScores = function() {
			$http.post('http://regdili.hf.ntnu.no:5051/server/get_scores').then(
				function(result) {
					var data = JSON.parse(result.data);
					$scope.scores = data["scores"];
				}, function() {
				});
		};

	$scope.getScores();
});
