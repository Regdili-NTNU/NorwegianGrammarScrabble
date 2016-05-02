// Helper function to convert words from a string to a pair (word, used?)
tagUnused = function(words) {
		var wordList = [];
		for (index in words) {
			var taggedWord = {word:words[index], used:false};
 			wordList.push(taggedWord);
		}
		return wordList;
};

// Helper function to fetch the list of words.
getWords = function(taggedWords) {
  var wordList = [];
  for (index in taggedWords) {
    var taggedword = taggedWords[index]
    if (!taggedword.used) {
      wordList.push(taggedword.word);
    }
  }
  return wordList;
};

app.controller("playController", function($scope, $http, $mdDialog, $location, $routeParams, translationService, pointService) {
	$scope.ts = translationService;
	if ($routeParams.language) {
		$scope.ts.setLanguage($routeParams.language);
	}

	$scope.pointService = pointService;
	$scope.pointService.score = 0;

	$scope.responses = [];
	$scope.words = [];
	$scope.loading = false;


	$scope.analyze = function() {
		var request = {sentence:$scope.textInput, words:getWords($scope.words), language:$scope.ts.getLanguage()};
		$scope.loading = true;
		$http.post('http://regdili.hf.ntnu.no:5051/server/parse', request)
			.then(function successCallback(response) {
				$scope.loading = false;
				var data = JSON.parse(response.data);
				var response = {text:data.original_sentence};
				if (data.error) {
					response.error = data.error;
				} else {
					response.score = data.score;
					response.malfeedback = data.malfeedback;
					response.suggestion = data.suggestion;
					$scope.pointService.score += data.score;
					$scope.markWordsAsUsed(data.used_words);
				}
				$scope.responses.unshift(response);
			}, function failureCallback(response) {
				$scope.loading = false;
				alert("Call failed!");
			});
	};

	$scope.remove = function(index) {
		$scope.responses.splice(index, 1);
	}	

	$scope.generateWords = function() {
		$http.get('http://regdili.hf.ntnu.no:5051/server/words')
			.then(
				function successCallback(response) {
					var data = JSON.parse(response.data);
					$scope.words = tagUnused(data.words);
				}, function failureCallback(response) {
					alert("Couldn't populate words!");
				});
	}

	$scope.markWordsAsUsed = function(wordlist) {
		for (word in $scope.words) {
			if ($scope.words[word].used) {
				continue;
			}
			var index = wordlist.indexOf($scope.words[word].word);
			if (index != -1) {
				$scope.words[word].used = true;
				wordlist.splice(index, 1);
			}
		}
	}

	$scope.endGame = function(ev) {
		var namePrompt = $mdDialog.prompt()
			.title($scope.ts.great_work_string())
			.textContent($scope.ts.end_game_description_string())
   			.targetEvent(ev)
			.ok($scope.ts.end_game_string())
			.cancel($scope.ts.keep_playing_string());

		var endCallback = function(result) {
			var request = {'username' : result, 'score' : $scope.pointService.score}
			$http.post('http://regdili.hf.ntnu.no:5051/server/add_score', request).then(
				function(result) {
					$scope.pointService.score = undefined;
					$location.path("/start");
				}, function() {
					alert("Something went wrong. Please try again.");
				});
		};

		$mdDialog.show(namePrompt).then(endCallback, function() {});
	}

	$scope.generateWords()
});
