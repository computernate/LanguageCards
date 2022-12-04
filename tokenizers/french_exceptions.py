import geonamescache

def checkException(word, translation):
    if translation.capitalize() in geonamescache.GeonamesCache().get_countries_by_names().keys():
        return [
            {
                "Translations":[{"Language": 1, "Term": translation}],
                "BaseForm":word,
                "Forms":[{"Word":word, "Tags":["pays", "nom"]}],
                "Language":2
            }
        ]
    if word == "la":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "BaseForm":"la",
                "Forms":[{"Word":"la", "Tags":["article-défini", "feminine"]}],
                "Language":2
            }
        ]
    if word == "le":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "BaseForm":"le",
                "Forms":[{"Word":"le", "Tags":["article-défini", "masculine"]}],
                "Language":2
            }
        ]
    if word == "les":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "BaseForm":"les",
                "Forms":[{"Word":"les", "Tags":["article-défini", "plural"]}],
                "Language":2
            }
        ]
    if word == "l":
        return [
            {
                "Translations":[{"Language": 1, "Term": "the"}],
                "BaseForm":"l",
                "Forms":[{"Word":"l", "Tags":["article-défini"]}],
                "Language":2
            }
        ]
    return None