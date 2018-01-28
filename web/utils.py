import json 
import boto3
import config

with open('./dict/out.json') as f:
    glossary = json.load(f)


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


def add_sentence(word, desc, return_sentence):
    if desc:
        return_sentence.append({'word' : word, 'desc' : desc})
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

    # print(text, sentences)
    for i in range(0, len(sentences), 1):
        #three word dict
        contin = True
        word = sentences[i]
        desc = None

        #if word is in blacklist then continue and add it to the list as a string

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

        return_sentence = add_sentence(word, desc, return_sentence)


    return return_sentence

    #one word dict
    # for word in sentences:



# text = "a fine Abbacchio with a side of Amaretti topped with fresh shavings of Noce Moscata Bao bun"
# print(translate(text))

    

