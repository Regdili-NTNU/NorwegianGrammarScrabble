app.service('translationService', function($window) {
	this.getLanguage = function() {
		var languageString = $window.navigator.language;
		if (languageString.indexOf('no') >= 0) {
			return "no";
		}
		return "en";
	};

	this.check_string = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Sjekk setninga"; 
		}
		return "Check";
	}

	this.checking_string = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Sjekker..."; 
		}
		return "Checking...";
	}

	this.description_string_1 = function() {
		var language = this.getLanguage();
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
	
	this.description_string_2 = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Last inn sida på nytt for å starte en ny runde.";
		}
		return "Refresh the browser to start a new game.";
	}	

	this.description_string_3 = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Hvis du har tilbakemeldinger eller kommentarer, ta gjerne kontakt " +
				"på e-post: elias.aamot@gmail.com"; 
		}
		return "For comments and feedback, contact elias.aamot@gmail.com";
	}	

	this.end_game_string = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Avslutt runden"; 
		}
		return "End game";
	}

	this.enter_sentence_string = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Skriv inn setninga di her"; 
		}
		return "Enter sentence here";
	}

	this.high_score_string = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Poengtavle"; 
		}
		return "High score";
	}

	this.no_score_string = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Ingen har ennå registert en poengsum. Spill en runde for å bli den første!"; 
		}
		return "No scores have been registered yet. Play a round to be the first!";
	}

	this.start_new_game_string = function() {
		var language = this.getLanguage();
		if (language == "no") {
			return "Start ny runde"; 
		}
		return "Start new game";
	}
});
