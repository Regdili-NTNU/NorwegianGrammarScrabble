app.controller("scoresController", function($scope, $http, $mdDialog, $window) {
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

	/**
	 * I18n functions
	 */

	$scope.getLanguage = function() {
		var languageString = $window.navigator.language;
		if (languageString.indexOf('no') >= 0) {
			return "no";
		}
		return "en";
	};

	$scope.high_score_string = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Poengtavle"; 
		}
		return "High score";
	}

	$scope.no_score_string = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Ingen har ennå registert en poengsum. Spill en runde for å bli den første!"; 
		}
		return "No scores have been registered yet. Play a round to be the first!";
	}

	$scope.start_new_game_string = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Start ny runde"; 
		}
		return "Start new game";
	}

});
