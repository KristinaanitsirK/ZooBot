import telebot
from telebot import types
from config import (TOKEN, QUESTIONS, COMMANDS, ANIMAL_IMAGES,
                    UserData, get_animal_facts, validate_animal,
                    get_facts_text)
from extensions import (BOTException, AnimalNotFoundException,
                        AnimalImageNotFoundException, InvalidCommandException)



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', ])
def start_message(message):
    start_text = (f"Привет, {message.chat.first_name}. \n"
"\n"
"Данный бот создан для популяризации программы опеки Московского Зоопарка.\
Мы придумали для Вас викторину, на тему 'Какое твоё тотемное животное?' \
Чтобы пройти тест, напиши мне /quiz и я скажу тебе, какое именно твоё тотемное животное. \
Для того, чтобы узнать больше возможностей данного бота, напиши /help.")
    bot.send_message(message.chat.id, start_text)


@bot.message_handler(commands=['help', ])
def help_message(message: telebot.types.Message):
    text = 'Доступные команды бота: ' + '\n'
    for key, value in COMMANDS.items():
        text += f'{key}: {value};\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['care'])
def info(message: telebot.types.Message):
    text = ('Участие в программе «Клуб друзей зоопарка» — это помощь в содержании \
наших обитателей, а также ваш личный вклад в дело сохранения биоразнообразия Земли \
и развитие нашего зоопарка. Традиция опекать животных в Московском зоопарке возникло \
с момента его создания в 1864г.'
"\n"
    'Опекать – значит помогать любимым животным. Взять под опеку можно разных \
обитателей зоопарка, например, слона, льва, суриката или фламинго. Почётный статус \
опекуна позволяет круглый год навещать подопечного, быть в курсе событий его жизни и самочувствия.'
"\n"
'Чтобы познакомиться получше с нашей программой опеки, \
предлагаю посетить нашу домашнюю страничку: https://moscowzoo.ru/about/guardianship')
    bot.reply_to(message, text)


quiz_data = {}

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    user_id = message.from_user.id

    if user_id not in quiz_data:
        quiz_data[user_id] = UserData(user_id)
    else:
        quiz_data[user_id].reset()

    send_question(user_id)

def send_question(user_id):
    user = quiz_data[user_id]
    question_index = user.current_question

    if question_index < len(QUESTIONS):
        question_data = QUESTIONS[question_index]
        question_text = question_data['question']
        answers = question_data['answers']

        markup = types.InlineKeyboardMarkup()
        for answer in answers.keys():
            markup.add(types.InlineKeyboardButton(text=answer, callback_data=f'{question_index}:{answer}'))

        bot.send_message(user_id, question_text, reply_markup=markup)
    else:
        determine_winner(user_id)


@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def restart_quiz(call):
    user_id = call.from_user.id
    quiz_data[user_id].reset()
    start_quiz(call)


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    user_id = call.from_user.id
    user = quiz_data[user_id]
    question_index = user.current_question
    question_data = QUESTIONS[question_index]
    answers = question_data['answers']

    _, selected_answer = call.data.split(':')
    selected_answer = next((key for key in answers if key.startswith(selected_answer)))

    if selected_answer:
        user.score(answers[selected_answer])

    user.current_question += 1
    send_question(user_id)


def determine_winner(user_id):
    user = quiz_data[user_id]
    winner = user.get_winner()
    image_path = ANIMAL_IMAGES.get(winner)
    facts = get_animal_facts(winner)

    send_animal_info(user_id, winner, image_path, facts)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Попробовать ещё раз', callback_data='restart'))

    bot.send_message(user_id, 'Если хочешь узнать интересные факты о других животных, \
то напиши /animals и получишь полный список животных', reply_markup=markup)


def send_animal_info(chat_id, animal, image_path, facts):
    if image_path:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=f'Ваше тотемное животное: {animal}!')

    if facts:
        facts_text = get_facts_text(animal, facts)
        bot.send_message(chat_id, f'Вот три интересных факта о животном {animal}:\n\n{facts_text}')
    else:
        raise AnimalNotFoundException(animal)

@bot.message_handler(commands=['animals'])
def animals_list(message):
    animals = '\n'.join(ANIMAL_IMAGES.keys())
    text = ('Чтобы узнать интересные факты об интересуюшем тебя животном, просто напиши мне его название!')
    bot.send_message(message.chat.id, f'Доступные животные:\n \n {animals} \n \n {text}')


@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    animal = message.text.lower()
    try:
        if message.text.startswith('/'):
            command = message.text.split()[0]
            if command not in COMMANDS:
                raise InvalidCommandException(command)

        validate_animal(animal, ANIMAL_IMAGES)
        facts = get_animal_facts(animal)
        image_path = ANIMAL_IMAGES.get(animal)

        if not image_path:
            raise AnimalImageNotFoundException(animal)

        send_animal_info(message.chat.id, animal, image_path, facts)

    except AnimalNotFoundException as e:
        bot.reply_to(message, str(e))
    except InvalidCommandException as e:
        bot.reply_to(message, e)
    except BOTException as e:
        bot.reply_to(message, e)


bot.polling(none_stop=True)