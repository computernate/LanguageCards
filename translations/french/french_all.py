from translations.french.french_english import translate_english_french


def get_french_translations(word):
    #This will probably need to be updated one day to scrape multiple translations and languages
    english_translations = {"Language": 1, "Term": translate_english_french(word)}
    return [english_translations, ]