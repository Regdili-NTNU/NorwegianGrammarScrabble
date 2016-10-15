app.service('translationService', function($window) {
	this.language = undefined;
	
	this.setLanguage = function(lang) {
		this.language = lang;
	};
	
	this.getLanguage = function() {
		if (this.language != undefined) {
			return this.language;
		}
		
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
	this.start_new_game_string_no = function() {
		 return "Start ny runde (Norsk)";
	};
	this.start_new_game_string_en = function() {
		 return "Start new game (english)";
	};
	this.start_new_game_string_pl = function() {
		 return "Start new game (polish)";
	};
	this.start_new_game_string_it = function() {
		 return "Start new game (italiano)";
	};
	this.start_new_game_string_de = function() {
		 return "Neues Spiel (Deutsch)";
	};
	this.start_new_game_string_zh = function() {
		 return "Start new game (zhongwen)";
	};
	this.start_new_game_string_ar = function() {
		 return "Start new game (arabic)";
	};
	this.start_new_game_string_bg = function() {
		 return "Start new game (bulgarian)";
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

	this.checking_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Sjekker...';
		}
		return 'Checking...';
	}

	this.points_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'poeng';
		}
		return 'points';
	}

	this.all_time_high_score_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Poengtavle';
		}
		return 'High Score';
	}

	this.weekly_high_score_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Ukas beste';
		}
		return 'High score of the week';
	}

	this.great_work_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Bra jobba!';
		}
		return 'Great work!';
	}

	this.keep_playing_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Spill videre';
		}
		return 'Keep playing';
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
			return 'Last inn sida på nytt for å starte en ny runde.';
		}
		return 'Refresh the browser to start a new game.';
	}

	this.description_string_1 = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Bruk ordene du har fått tildelt til å utforme grammatisk korrekte setninger på norsk. Substantiv, adjektiv og verb er oppgitt i ordbokform. Disse må du bøye for å bygge setninger med dem. Andre ord kan kun bli brukt i forma som er oppgitt.';
		}
		return 'Use the provided words to form grammatical Norwegian sentences. Nouns, adjectives and verbs are provided in their basic form. These have to be inflected when put together to sentences. Other words can only be used in the form provided.';
	}

	this.end_game_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Avslutt runden';
		}
		return 'End game';
	}

	this.end_game_description_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Fyll inn et navn for få poengsummen din inn på rekordtavla.';
		}
		return 'Please enter a name to go with your score.';
	}

	this.suggested_correction_string = function() {
		var language = this.getLanguage();
		if (language == 'no') {
			return 'Vi foreslår i stedet';
		}
		return 'Suggested correction';
	}
});