
#setup stuff
from google.cloud import translate
translate_client = translate.Client()


#replace this with the json object containing the parsed words
text = 'Hello, world!'


#user should be able to pick which language imo
selected_language = 'en'

translate = translate_client.translate(
    text,
    target_language=selected_language)

print(translate)

#to get just the the translated text - use translate['translatedText']
