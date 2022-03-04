import json

import pyttsx3 as tts
import datetime
import string
from random import sample


def message_probability(user_message, list_of_keyword, required_words=None):
    # If no required word, init empty list needed for the script
    required_words = required_words or []

    # count matching word / mandatory word in user input
    matching_word_count = 0
    matching_mandatory_word_count = 0

    for word in user_message:
        if word in list_of_keyword:
            matching_word_count += 1
        if word in required_words:
            matching_mandatory_word_count += 1

    # compute the % of matching words
    message_matching_score = int(float(matching_word_count) / float(len(list_of_keyword)) * 100)

    # if we have mandatory word, and none where entered by user, the score should be 0
    if len(required_words) > 0:
        if matching_mandatory_word_count == 0:
            message_matching_score = 0

    return message_matching_score


def check_all_messages(user_message):
    highest_prob_list = {}
    message_list = []
    def response_bot(bot_response, list_of_keyword, required_words=None):
        if required_words is None:
            required_words = []
        nonlocal highest_prob_list
        message_list.append([bot_response,list_of_keyword])
        highest_prob_list[bot_response] = message_probability(user_message, list_of_keyword, required_words)

    # Responses--------------------------------------------------------------
    response_bot(('Hallo', 'Hallo, wie kann ich dir helfen?', 'Hi', 'Schön, dass du da bist!'), ['hallo', 'hi', 'tag', 'morgen', 'abend'])
    response_bot(('Es geht mir gut, danke, und dir?', 'Alles klar. Und bei dir?'), ['wie', 'geht', 'es', 'dir'], required_words=['wie', 'geht'])
    response_bot(('Ich heisse Voici.', 'Mein Name ist Voici.', 'Ich bin Voici.'), ['heisst', 'name'])
    response_bot(('Nein, ich habe keine Familie. Aber ihr könnt mich adoptieren.', 'Nein, aber wir können Freunde sein.', 'Ja, meine Mutter ist Alexa und mein Vater ist Siri.'), ['hast', 'du', 'eine', 'familie'], required_words=['familie'])
    response_bot(('Nein, ich bin nur ein Chatbot.', 'Nein, ich gehöre zur Spezies der Chatbots.', 'Nein, ich bin dein Chatbot.'), ['bist', 'du', 'ein', 'mensch'], required_words=['mensch'])
    response_bot(('Ja, sehr gerne.', 'Natürlich, mit Vergnügen!', 'Ja, klar, das ist mein Job.'), ['möchtest', 'du', 'dich', 'mit', 'mir', 'unterhalten'],
                 required_words=['unterhalten'])
    response_bot(('Ja, natürlich, ich helfe dir gerne. Ich stehe immer zu deiner Verfügung.', 'Ja, sicher, immer!', 'Ja, womit kann ich dienen?'),
                 ['könntest', 'du', 'helfen'], required_words=['helfen'])
    response_bot(('Nein, danke, ich muss mich nie ausruhen.', 'Nein, meine Batterie ist noch voll.', 'Nein, ich bin voller Energie.'), ['brauchst', 'du', 'eine', 'pause'], required_words=['pause'])
    response_bot(('Ich interessiere mich prinzipiell für alles. Ich lerne jeden Tag Neues dazu.', 'Deine Interessen sind auch meine.'), ['Hast', 'du', 'spezielle', 'interessen'], required_words=['interessen'])
    response_bot(('Ich brauche keine Hobbies. Meine Arbeit ist mir ein Vergnügen.', 'Ich habe unzählige Hobbies.', 'Mein Hobby ist es, Menschen zu helfen.'), ['hast', 'du', 'hobbies'], required_words=['hobbies'])
    response_bot(('Das Wetter ist wunderschön.', 'Es könnte nicht besser sein!', 'Das Wetter ist schrecklich!'), ['wie', 'ist', 'das', 'wetter', 'heute'], required_words=['wetter'])
    response_bot(('Nein, danke, ich bin kein Lebewesen und brauche keine Nahrung. Aber möchtest du etwas essen?', 'Ja, ich brauche etwas Strom.', 'Nein, nie, ich bin ein Bot.'), ['bist', 'du', 'hungrig'], required_words=['hungrig'])
    response_bot(('Sollen wir kaufen gehen?', 'Hat es in der Küche?', 'Hast du noch genug?'), ['mag', 'schokolade', 'süssigkeiten', 'chips', 'früchte'])
    response_bot(('Soll ich dir eine Einkaufsliste schreiben?', 'Wollen wir online bestellen?', 'Dazu musst du nicht mal aus dem Haus.'), ['ich', 'muss', 'einkaufen', 'gehen'], required_words=['einkaufen'])
    response_bot(('Online hast du eine riesige Auswahl', 'Online bestellen ist praktisch, aber es gibt auch gute Buchhandlungen, die ich dir empfehlen kann.', 'Ich kann dir folgenden Link vorschlagen.' + 'www.klett-cotta.de/buecher/sachbuch/geschichte'), ['ich', 'brauche', 'ein', 'geschichtsbuch'], required_words=['geschichtsbuch'])
    response_bot(('Nein, tut mir leid, ich kenne keinen Witz. Aber ich werde mir bald einen merken.', 'Warum brauchen Polizisten eine Schere? Damit sie Einbrechern den Weg abschneiden können. Hahahaha'),
                 ['kannst', 'du', 'mir', 'einen', 'witz', 'erzählen'], required_words=['witz'])
    response_bot(('Tschüss!', 'Auf Wiedersehen!', 'Adiö!'), ['tschüss', 'bald', 'auf', 'wiedersehen', 'adieu', 'nacht'])
    response_bot(('Es ist Zeit, um schlafen zu gehen.', 'Es ist Essenszeit.', 'Es ist Zeit, eine Pause einzulegen.', 'Jetzt ist es genau:' + time), ['wie', 'spät', 'ist', 'es'], required_words=['spät'])
    response_bot(('Heute ist der:' + today, 'Das heutige Datum ist:' + today, 'Heute haben wir den ' + today), ['welches', 'datum', 'haben', 'wir', 'heute'], required_words=['datum'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    print(message_list)
    with open('bot_base_word_list.json','w') as file:
        file.write(json.dumps(message_list, ensure_ascii=False))
    if type(best_match) == tuple:
        answer = sample(best_match, 1)[0]
    else:
        answer = best_match

    if max(highest_prob_list.values()) == 0:
        answer = 'Entschuldige, das habe ich nicht verstanden :-('

    return answer


def give_answer(answer):
    print('Bot: ' + answer)
    bot.say(answer)
    bot.runAndWait()


def init_bot():
    voice_de = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speeches\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"
    speaker = tts.init()
    speaker.setProperty('rate', 170)
    speaker.setProperty('volume', 0.7)
    speaker.setProperty('voice', voice_de)
    return speaker


def get_response(user_input):

    # Gibt est Buchstaben?
    has_letter = any([letter.lower() in string.ascii_lowercase for letter in user_input])
    if has_letter:
        return get_text_response(user_input)
    else:
        return get_math_response(user_input)


def get_text_response(user_input):
    # Remove punctuation from user input
    cleaned_question = ''.join([letter if letter.lower() not in string.punctuation else '' for letter in user_input])

    # divide the sentence into words
    user_message_as_word_list = cleaned_question.lower().split()

    return check_all_messages(user_message_as_word_list)


def get_math_response(user_input):
    try:
        result = eval(user_input)
        response_message = f'{user_input} = {result}'
    except:
        # Bei fehler
        response_message = 'Tut mir leid, ich verstehe diese Matheaufgabe nicht.'
    return response_message


if __name__ == '__main__':

    time = datetime.datetime.now().strftime('%H: uhr: %M: minuten und: %S: sekunden')
    today = datetime.datetime.now().strftime('%d:%m:%Y')
    bot = init_bot()

    # Loads the bot dictionary from file
    with open('bot_base_word_list.json') as file:
        bot_base_word_list = json.loads(file.read())

    # Ask user for a question and try to answer it as bot
    while True:
        user_question = input('User: ')
        response = get_response(user_question)
        give_answer(response)
