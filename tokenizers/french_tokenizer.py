from bs4 import BeautifulSoup
import requests
from translations.french.french_all import get_french_translations
from tokenizers.french_exceptions import checkException
from google.cloud import translate_v2

def tokenize(word):
    translate_client = translate_v2.Client()
    translation = translate_client.translate(word, target_language="en-US")['translatedText']
    returnWords = []

    #Check exceptions. This includes countries and stuff
    exception = checkException(word, translation)
    if(exception): return exception

    #Get some initial tags
    trans_data = requests.get("https://www.larousse.fr/dictionnaires/francais/{}".format(word))
    soup = BeautifulSoup(trans_data.text, 'html.parser')
    initialTags = soup.select("#definition h2.AdresseDefinition")
    for initialTag in initialTags:
        word_base = initialTag.contents[3]
        first_tags = initialTag.next_sibling.next_sibling.contents[0].string

        # This looks complicated. All it does is add unique tags to the list
        # if the word is already in the list.
        already_used = [
            index for index in range(len(returnWords))
            if returnWords[index]['BaseForm']==word_base
        ]
        if already_used:
            for i in range(len(returnWords[already_used[0]]['Forms'])):
                all_tags = returnWords[already_used[0]]['Forms'][i]['Tags'] + [x for x in first_tags.split(' ') if x]
                returnWords[already_used[0]]['Forms'][i]['Tags'] = list(set(all_tags))
            continue


        #If it is a verb
        if 'verbe' in first_tags:
            try:
                link = initialTag.next_sibling.next_sibling.contents[1]['href']
            except:
                continue
            conj_data = requests.get("https://www.larousse.fr{}".format(link))
            link_soup = BeautifulSoup(conj_data.text, 'html.parser')
            auxillary = link_soup.select('.groupe.aux a')[0].text
            verb_map=[
            #INDICATIF
                #PRESENT
                {'index': 0, 'tags':['indicatif', 'Présent', 'Je-Présent']},
                {'index': 1, 'tags':['indicatif', 'Présent', 'Tu-Présent']},
                {'index': 2, 'tags':['indicatif', 'Présent', 'Il/Elle-Présent']},
                {'index': 3, 'tags':['indicatif', 'Présent', 'Nous-Présent']},
                {'index': 4, 'tags':['indicatif', 'Présent', 'Vous-Présent']},
                {'index': 5, 'tags':['indicatif', 'Présent', 'Ils/Elles-Présent']},
                #Impartfait
                {'index': 6, 'tags':['indicatif', 'Imparfait', 'Je-Imparfait']},
                {'index': 7, 'tags':['indicatif', 'Imparfait', 'Tu-Imparfait']},
                {'index': 8, 'tags':['indicatif', 'Imparfait', 'Il/Elle-Imparfait']},
                {'index': 9, 'tags':['indicatif', 'Imparfait', 'Nous-Imparfait']},
                {'index': 10, 'tags':['indicatif', 'Imparfait', 'Vous-Imparfait']},
                {'index': 11, 'tags':['indicatif', 'Imparfait', 'Ils/Elles-Imparfait']},
                #Passe simple
                {'index': 12, 'tags':['indicatif', 'Passé simple', 'Je-Passé simple']},
                {'index': 13, 'tags':['indicatif', 'Passé simple', 'Tu-Passé simple']},
                {'index': 14, 'tags':['indicatif', 'Passé simple', 'Il/Elle-Passé simple']},
                {'index': 15, 'tags':['indicatif', 'Passé simple', 'Nous-Passé simple']},
                {'index': 16, 'tags':['indicatif', 'Passé simple', 'Vous-Passé simple']},
                {'index': 17, 'tags':['indicatif', 'Passé simple', 'Ils/Elles-Passé simple']},
                #Futur
                {'index': 18, 'tags':['indicatif', 'Futur', 'Je-Futur']},
                {'index': 19, 'tags':['indicatif', 'Futur', 'Tu-Futur']},
                {'index': 20, 'tags':['indicatif', 'Futur', 'Il/Elle-Futur']},
                {'index': 21, 'tags':['indicatif', 'Futur', 'Nous-Futur']},
                {'index': 22, 'tags':['indicatif', 'Futur', 'Vous-Futur']},
                {'index': 23, 'tags':['indicatif', 'Futur', 'Ils/Elles-Futur']},
            #Subjonctif
                #PRESENT
                {'index': 48, 'tags':['Subjonctif', 'Présent', 'Je-Présent']},
                {'index': 49, 'tags':['Subjonctif', 'Présent', 'Tu-Présent']},
                {'index': 50, 'tags':['Subjonctif', 'Présent', 'Il/Elle-Présent']},
                {'index': 51, 'tags':['Subjonctif', 'Présent', 'Nous-Présent']},
                {'index': 52, 'tags':['Subjonctif', 'Présent', 'Vous-Présent']},
                {'index': 53, 'tags':['Subjonctif', 'Présent', 'Ils/Elles-Présent']},
                #imparfait
                {'index': 54, 'tags':['Subjonctif', 'Imparfait', 'Je-Imparfait']},
                {'index': 55, 'tags':['Subjonctif', 'Imparfait', 'Tu-Imparfait']},
                {'index': 56, 'tags':['Subjonctif', 'Imparfait', 'Il/Elle-Imparfait']},
                {'index': 57, 'tags':['Subjonctif', 'Imparfait', 'Nous-Imparfait']},
                {'index': 58, 'tags':['Subjonctif', 'Imparfait', 'Vous-Imparfait']},
                {'index': 59, 'tags':['Subjonctif', 'Imparfait', 'Ils/Elles-Imparfait']},
            #Other
                {'index': 90, 'tags':['Participe', 'Présent']},
                {'index': 91, 'tags':['Participe', 'Passé-composé']},
            ]

            forms = []
            raw_words = link_soup.select('.verbe')

            for item in verb_map:
                already_used = [
                    index for index in range(len(forms))
                    if forms[index]['Word'] == raw_words[item['index']].text
                ]
                if already_used:
                    all_tags = forms[already_used[0]]['Tags'] + item['tags']
                    forms[already_used[0]]['Tags'] = list(set(all_tags))
                    continue

                item['tags'].append("aux. {}".format(auxillary))
                forms.append({
                    'Word':raw_words[item['index']].text,
                    'Tags': item['tags'] + [x for x in first_tags.split(' ') if x]
                })

            returnWords.append({
                'BaseForm':word_base,
                'Forms':forms,
                'Language':2,
                'Translations': get_french_translations(word_base)
            })

        elif first_tags == 'adjectif' or first_tags == 'adverbe':
            conj_data = requests.get("https://conjf.cactus2000.de/show_adj.en.php?adj={}".format(word_base))
            link_soup = BeautifulSoup(conj_data.text, 'html.parser')
            gendered = link_soup.select('table.conjtab tr:nth-child(3) td')
            masculine = gendered[1] if len(gendered)>1 else None
            feminine = gendered[2] if len(gendered)>2 else None
            adverb_select = link_soup.select('table.conjtab tr:nth-child(8) td')
            adverb = adverb_select[1] if len(adverb_select)>1 else None
            forms = []
            if(masculine and len(masculine.contents)>0): forms.append({'Word': masculine.contents[0], 'Tags': ['Masculin', 'Singulier', 'Masculin-Singulier', 'Adjective']})
            if(masculine and len(masculine.contents)>2): forms.append({'Word': masculine.contents[2], 'Tags': ['Masculin', 'Plural', 'Masculin-Plural', 'Adjective']})
            if(feminine and len(feminine.contents)>0): forms.append({'Word': feminine.contents[0], 'Tags': ['Féminin', 'Singulier', 'Féminin-Singulier', 'Adjective']})
            if(feminine and len(feminine.contents)>2): forms.append({'Word': feminine.contents[2], 'Tags': ['Féminin', 'Plural', 'Féminin-Plural', 'Adjective']})
            if(adverb  and len(adverb.contents)>0): forms.append({'Word': adverb.contents[0], 'Tags': ['Adverbe']})
            returnWords.append({
                'BaseForm':word_base,
                'Forms':forms,
                'Language':2,
                'Translations': get_french_translations(word_base)
            })
        elif 'pronom personnel' in first_tags:
            returnWords.append({
                'BaseForm':word_base,
                'Forms':[
                    {'Word': word_base, 'Tags': ['prenom-personnel']}
                ],
                'Language':2,
                'Translations': get_french_translations(word_base)
            })

        elif 'nom' in first_tags:
            conj_data = requests.get("http://conjugation.sensagent.com/fr/{}".format(word_base))
            link_soup = BeautifulSoup(conj_data.text, 'html.parser')
            raw_forms = link_soup.select('table.infls')
            if len(raw_forms)==0: continue
            raw_forms = raw_forms[0].select('td:nth-child(2)')
            forms = [
                {'Word': raw_forms[0].text, 'Tags': ['Masculin', 'Singulier', 'Nom']},
                {'Word': raw_forms[1].text, 'Tags': ['Masculin', 'Plural', 'Nom']},
                {'Word': raw_forms[2].text, 'Tags': ['Féminin', 'Singulier', 'Nom']},
                {'Word': raw_forms[3].text, 'Tags': ['Féminin', 'Plural', 'Nom']},
            ]
            forms = [form for form in forms if form['Word']!='/']
            returnWords.append({
                'BaseForm':word_base,
                'Forms':forms,
                'Language':2,
                'Translations': get_french_translations(word_base)
            })
        else:
            returnWords.append({
                'BaseForm':word_base,
                'Forms':[
                    {'Word': word_base, 'Tags': [x for x in first_tags.split(' ') if x]}
                ],
                'Language':2,
                'Translations': get_french_translations(word_base)
            })
    return returnWords

if __name__ == "__main__":
    #Words to add manually:
    """
        Avoir
        à
        le/la/les/l'
        un/une
        ne 
        ce/c'
    """
    #test = "Mercredi 9 novembre, la Commission présenté les grandes lignes de ce qui pourrait être une réforme en profondeur de ce texte en vertu duquel le déficit public ne doit pas dépasser"
    test = "présenté"
    for item in test.lower().split(' '):
        print(item)
        try:
            tokenize(item)
        except Exception as e:
            print('ERROR')
            print(e)