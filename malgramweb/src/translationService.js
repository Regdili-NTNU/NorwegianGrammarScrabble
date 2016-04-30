app.service('translationService', function($window) {
	this.getLanguage = function() {
		var languageString = $window.navigator.language;
		if (languageString.indexOf('no') >= 0) {
			return "no";
		}
		if (languageString.indexOf('pl') >= 0) {
			return "pl";
		}
		if (languageString.indexOf('it') >= 0) {
			return "it";
		}
		if (languageString.indexOf('de') >= 0) {
			return "de";
		}
		if (languageString.indexOf('zh') >= 0) {
			return "zh";
		}
		if (languageString.indexOf('ar') >= 0) {
			return "ar";
		}
		if (languageString.indexOf('bg') >= 0) {
			return "bg";
		}
		return "en";
	};
	
	this.getRtl = function() {
		 return this.getLanguage() == "ar" ? "rtl" : "ltr";
	};

	this.start_new_game_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Start ny runde';
		}
		return 'Start new game';
	}

	this.enter_sentence_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Skriv inn setninga di her';
		}
		return 'Enter sentence here';
	}

	this.check_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Sjekk setninga';
		}
		return 'Check';
	}

	this.no_score_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Ingen har ennå registert en poengsum. Spill en runde for å bli den første!';
		}
		return 'No scores have been registered yet. Play a round to be the first!';
	}

	this.high_score_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Poengtavle';
		}
		return 'High Score';
	}

	this.description_string_3 = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Hvis du har tilbakemeldinger eller kommentarer, ta gjerne kontakt på e-post: elias.aamot@gmail.com';
		}
		return 'For comments and feedback, contact elias.aamot@gmail.com';
	}

	this.description_string_2 = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Last inn sida på nytt for å start en ny runde.';
		}
		return 'Refresh the browser to start a new game.';
	}

	this.description_string_1 = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Bruk ordene du har fått tildelt til å utforme grammatisk korrekt setninger på norsk. Substantiv, adjektiv og verb er oppgitt i ordbokform. Disse må du bøye for å bygge setninger med dem. Andre ord kan kun bli brukt i forma som er oppgitt.';
		}
		return 'Use the provided words to form grammatical Norwegian sentences. Nous, adjectives and vers are provided in their basic form. These have to be inflected when put together to sentences. Other words can only be used in the form provided.';
	}

	this.end_game_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Avslutt runden';
		}
		return 'End game';
	}

	this.checking_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Sjekker...';
		}
		return 'Checking...';
	}
});