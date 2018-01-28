import json 
import boto3
import config

import requests

from bs4 import BeautifulSoup

with open('./dict/out.json') as f:
    glossary = json.load(f)

with open('./dict/blacklist.json') as f:
    blacklist = set(json.load(f)['blacklist'])

# KEY = "test_ocr.png"


def detect_text(img, region="us-east-1"):
    rekognition = boto3.client("rekognition", region, aws_access_key_id=config.secrets['aws_id'], aws_secret_access_key=config.secrets['aws_secret'])
    
    # with open(img, "rb") as imageFile:
    #       f = imageFile.read()
    #       img = bytearray(f)
      
    response = rekognition.detect_text(
        Image={
            'Bytes': img,
            }
        )

    return response

def google_translate(sentence):
    data = {
        'q' : sentence,
        'target': 'en',
    }

    url = "https://translation.googleapis.com/language/translate/v2?key=%s"%(config.secrets['google_key'])

    r = requests.post(url, data=data)

    if r.status_code == 200:
        return r.text
    else:
        print(r)
        print(r.status_code)
        return None

def get_image(query):
    cx = "010727462276892999876:q8hxbqk3uvq"
    url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&searchType=image&q=%s"%(config.secrets['google_key'], cx, query)
    r = requests.get(url)

    # print(r)
    # print(r.text)
    links = []
    i = 0
    # print(json.loads(r.text))
    goog_data = json.loads(r.text).get('items', [])
    while len(links) < 3 or not goog_data:
        i += 1
        
        print(goog_data[i]['image'].keys())
        a = goog_data[i].get('image', {}).get('thumbnailLink', None)#..get('link', None)
        if a:
            links.append(a)
        goog_data.pop()
    return links

def add_sentence(word, desc, return_sentence):
    if desc:
        return_sentence.append({'word' : word, 'desc' : desc, 'img':get_image(desc)})
    else:
        return_sentence.append(word)
    return return_sentence

def translate(raw_text):
    """
    takes text runs it through the dictionary to see if there are any doubles
    text : String
    """

    text = raw_text.strip().lower()
    sentences = text.split(' ')

    return_sentence = []
    pos = []
    # print(text, sentences)
    translate_words = []
    for i in range(0, len(sentences), 1):
        #three word dict
        contin = True
        word = sentences[i]
        desc = None

        #if word is in blacklist then continue and add it to the list as a string

        if word in blacklist:

            return_sentence = add_sentence(word, desc, return_sentence)
            continue

        if len(sentences)-2 > i:
            raw_word = sentences[i] + ' ' + sentences[i+1] + ' ' + sentences[i+2]
            
            if str(raw_word).lower() in glossary['3'].keys():
                # print(glossary['3'][word])
                word = raw_word
                desc = glossary['3'][word]
                contin = False

        #two word dict
        if len(sentences)-1 > i and contin :
            raw_word = sentences[i] + ' ' + sentences[i+1]
            if str(raw_word).lower() in glossary['2'].keys():
                # print(glossary['2'][raw_word])
                word = raw_word
                desc = glossary['2'][word]
                contin = False

        if contin:                
            raw_word = sentences[i]
            
            if str(raw_word).lower() in glossary['1'].keys():
                # print(glossary['1'][word])
                raw_word
                desc = glossary['1'][word]
                contin = False


        #if the item gets here before continuing then search for it on wikipedia and return the first sentance.
        
        if contin:
            # translate_words += "%s. "%word
            translate_words.append(word)
            pos.append((word, i))
            continue

        return_sentence = add_sentence(word, desc, return_sentence)

    try:
        if translate_words != []:
            goog_out = json.loads(google_translate(translate_words))
            # print(goog_out)

            #get translations, then insert the words back into return_sentence based off of the positions values in pos
            
            for k in range(len(goog_out['data']['translations'])):
                return_sentence.insert(pos[k][1], {'word' : pos[k][0], 'desc' : goog_out['data']['translations'][k]['translatedText'], 'img':get_image(goog_out['data']['translations'][k]['translatedText'])})

    except Exception as e:
        print(e)
        for k in pos:
            return_sentence.insert(k[1], k[0])
    
    # for i in pos:


    return return_sentence


    
# print(get_image('steak'))
# print(translate('a fine fait manger abbacchio cavolo'))