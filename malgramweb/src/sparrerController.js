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

app.controller("sparrerController", function($scope, $http, $mdDialog, $location, $window) {
	$scope.score = 0;
	$scope.responses = [];
	$scope.words = [];
	$scope.loading = false;

	$scope.analyze = function() {
		var request = {sentence:$scope.textInput, words:getWords($scope.words)};
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
					$scope.score += data.score;
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
			.title("Great work!")
			.textContent("Please enter a name to go with your score.")
			.ariaLabel("Enter your username")
   			.targetEvent(ev)
			.ok("End game")
			.cancel("Keep playing");

		var endCallback = function(result) {
			var request = {'username' : result, 'score' : $scope.score}
			$http.post('http://regdili.hf.ntnu.no:5051/server/add_score', request).then(
				function(result) {
					location.replace("scores.html");
				}, function() {
					alert("Something went wrong. Please try again.");
				});
		};

		$mdDialog.show(namePrompt).then(endCallback, function() {});
	}

	$scope.generateWords()

	/**
	 * I18n functions
	 */

	$scope.getLanguage = function() {
		var languageString = $window.navigator.language;
		if (languageString.indexOf('no') >= 0) {
			return "no";
		}
		return "en";
	}

	$scope.check_string = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Sjekk setninga"; 
		}
		return "Check";
	}

	$scope.checking_string = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Sjekker..."; 
		}
		return "Checking...";
	}

	$scope.description_string_1 = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Bruk ordene du har fått tildelt til å utforme grammatisk " +
				"korrekte setninger på norsk. Substantiv, adjektiv og verb er " +
				"oppgitt i ordbokform. Disse må du bøye for å bygge setninger " +
				"med dem. Andre ord kan kun bli brukt i forma som er oppgitt.";
		}
		return "Use the provided words to form grammatical Norwegian sentences. " +
		       "Nouns, adjectives and verbs are provided in their basic form. These " +
		       "have to be inflected when put together to sentences. Other words " +
		       "can only be used in the form provided.";
	}	
	
	$scope.description_string_2 = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Last inn sida på nytt for å starte en ny runde.";
		}
		return "Refresh the browser to start a new game.";
	}	

	$scope.description_string_3 = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Hvis du har tilbakemeldinger eller kommentarer, ta gjerne kontakt " +
				"på e-post: elias.aamot@gmail.com"; 
		}
		return "For comments and feedback, contact elias.aamot@gmail.com";
	}	

	$scope.end_game_string = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Avslutt runden"; 
		}
		return "End game";
	}

	$scope.enter_sentence_string = function() {
		var language = $scope.getLanguage();
		if (language == "no") {
			return "Skriv inn setninga di her"; 
		}
		return "Enter sentence here";
	}
});
