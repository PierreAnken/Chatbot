import json
import datetime
import string
from random import sample

try:
    import pyttsx3 as tts
except:
    raise Exception(f'missing library pyttsx3. Please install it with "pip install pyttsx3"')


def compute_message_probability(user_message, list_optional_keyword, list_required_keyword=None):
    # If no required word, init empty list needed for the script
    list_required_keyword = list_required_keyword or []

    # count matching word / mandatory word in user input
    matching_optional_keyword_count = 0
    matching_mandatory_keyword_count = 0

    for word in user_message:
        if word in list_optional_keyword:
            matching_optional_keyword_count += 1
        if word in list_required_keyword:
            matching_mandatory_keyword_count += 1

    # compute the % of matching words
    message_matching_score = int(float(matching_optional_keyword_count) / float(len(list_optional_keyword)) * 100)

    # if we have mandatory word, and none where entered by user, the score should be 0
    if len(list_required_keyword) > 0:
        if matching_mandatory_keyword_count == 0:
            message_matching_score = 0

    return message_matching_score


def get_highest_match_answer(user_input_cleaned):
    # bot_base_word_list contains [list_answer, list_optional_keyword, list_required_keyword]
    # for each pre-defined text in bot dictionary

    max_matching_score = -1
    highest_response_list = []

    # for each question the bot was trained for
    for bot_dictionary_entry in bot_dictionary:

        # get the matching score of the question
        matching_score = compute_message_probability(user_input_cleaned, bot_dictionary_entry['list_optional_keyword'], bot_dictionary_entry['list_required_keyword'])

        # if the score is higher then the previous higher one, we overwrite it
        if matching_score > max_matching_score:
            max_matching_score = matching_score
            highest_response_list = bot_dictionary_entry['list_answer']

    # if the matching score is 0
    if max_matching_score == 0:
        answer = 'Entschuldige, das habe ich nicht verstanden :-('

    else:
        # chose randomly from one of the known answers
        answer = sample(highest_response_list, 1)[0]

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

    # if there is at least a letter this is a question else a mathematical expression
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
    return get_highest_match_answer(user_message_as_word_list)


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

    # initalize sound
    bot = init_bot()

    # Loads the bot dictionary from file
    with open('bot_dictionary.json') as file:
        bot_dictionary = json.loads(file.read())

    # Ask user for a question and try to answer it as a bot
    while True:
        user_question = input('User: ')
        response = get_response(user_question)
        give_answer(response)
