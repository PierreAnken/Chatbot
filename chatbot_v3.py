import datetime
import json
import os
import string
from random import sample
from time import sleep
try:
    import pyglet
except:
    raise Exception(f'Missing library pyglet. Please install it with "pip install pyglet"')
try:
    from gtts import gTTS
except:
    raise Exception(f'Missing library gtts. Please install it with "pip install gtts"')


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
        if matching_mandatory_keyword_count != len(list_required_keyword):
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

        # check learned dictionary
        # for each question the bot was trained for
        for bot_dictionary_entry in bot_learned_answers:

            # get the matching score of the question
            matching_score = compute_message_probability(user_input_cleaned, bot_dictionary_entry['list_optional_keyword'], bot_dictionary_entry['list_required_keyword'])

            # if the score is higher then the previous higher one, we overwrite it
            if matching_score > max_matching_score:
                max_matching_score = matching_score
                highest_response_list = bot_dictionary_entry['list_answer']

        if max_matching_score == 0:
            # When the bot did not had an answer
            answer_saved = save_new_learned_question(user_input_cleaned)
            if answer_saved:
                if user_language == 'de':
                    answer = 'Danke für das Hinweis!'
                elif user_language == 'en':
                    answer = 'Thank you for the hint!'
                else:
                    answer = 'Merci de ton aide!'
            else:
                answer = None
        else:
            # chose randomly from one of the known answers
            answer = sample(highest_response_list, 1)[0]
    else:
        # chose randomly from one of the known answers
        answer = sample(highest_response_list, 1)[0]

    return answer


def save_new_learned_question(user_input_cleaned):

    # say we did not understand the question
    if user_language == 'de':
        bot_answer = 'Entschuldige, das habe ich nicht verstanden'
        bot_question = 'Was wäre für euch ein richtige antwort? '

    elif user_language == 'en':
        bot_answer = 'Sorry I did not understood you'
        bot_question = 'What would be a right answer for you? '

    else:
        bot_answer = 'Désolé je ne t ai pas compris.'
        bot_question = 'Comment tu répondrais à cette question?'

    give_answer(bot_answer)

    # remove small words from user question
    user_input_cleaned = [user_word for user_word in user_input_cleaned if len(user_word) > 3]

    # only save the answer if we have at least 2 long words in the question
    if len(user_input_cleaned) > 1:
        give_answer(bot_question)
        correct_answer = input('... : ')
        new_learned_dictionary = {
            'list_answer': [correct_answer],
            'list_optional_keyword': user_input_cleaned,
            'list_required_keyword': []
        }
        bot_learned_answers.append(new_learned_dictionary)
        with open(f'learned_answers_{user_language}.json', 'w') as file2:
            file2.write(json.dumps(bot_learned_answers, ensure_ascii=False))
        return True
    return False


def give_answer(answer):
    print('Bot: ' + answer)

    tts_text = gTTS(answer, lang=user_language)
    filename = 'temp.mp3'
    tts_text.save(filename)

    music = pyglet.media.load(filename, streaming=False)
    music.play()

    sleep(music.duration)
    os.remove(filename)


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

    user_language = ''
    while user_language not in ('de', 'en', 'fr'):
        user_language = input('What is your language? (de/en/fr)')


    # Loads the bot dictionary from file
    with open(f'bot_dictionary_{user_language}.json') as file:
        bot_dictionary = json.loads(file.read())

    # Loads the bot learned question from file
    with open(f'learned_answers_{user_language}.json') as file:
        bot_learned_answers = json.loads(file.read())

    # Ask user for a question and try to answer it as a bot
    while True:
        user_question = input('User: ')
        response = get_response(user_question)
        if response:
            give_answer(response)
