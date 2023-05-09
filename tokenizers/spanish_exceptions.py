import geonamescache

def checkException(word, translation):
    if translation.capitalize() in geonamescache.GeonamesCache().get_countries_by_names().keys():
        return [
            {
                "Translations":[{"Language": 1, "Term": translation}],
                "BaseForm":word,
                "Forms":[{"Word":word, "Tags":["pays", "nom"]}],
                "Language":3
            }
        ]