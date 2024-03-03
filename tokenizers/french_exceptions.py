import geonamescache

def checkException(word, translation):
    if translation.capitalize() in geonamescache.GeonamesCache().get_countries_by_names().keys():
        return [
            {
                "Translations":[{"Language": 1, "Term": translation}],
                "Base":word,
                "Inflections":[{"Word":word, "Tags":["pays", "nom"]}],
                "Language":2
            }
        ]
    if word == "la":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "Base":"la",
                "Inflections":[{"Word":"la", "Tags":["article-défini", "feminine"]}],
                "Language":2
            }
        ]
    if word == "le":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "Base":"le",
                "Inflections":[{"Word":"le", "Tags":["article-défini", "masculine"]}],
                "Language":2
            }
        ]
    if word == "les":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "Base":"les",
                "Inflections":[{"Word":"les", "Tags":["article-défini", "plural"]}],
                "Language":2
            }
        ]
    if word == "l":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "Base":"l",
                "Inflections":[{"Word":"l", "Tags":["article-défini"]}],
                "Language":2
            }
        ]
    if word == "d":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "Base":"d",
                "Inflections":[{"Word":"d", "Tags":["article"]}],
                "Language":2
            }
        ]
    return None