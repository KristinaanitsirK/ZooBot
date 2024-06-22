import docx
from dotenv import load_dotenv
import os
from extensions import AnimalNotFoundException

load_dotenv()

TOKEN = os.getenv('TOKEN')

ANIMAL_IMAGES = {
    'капибара': 'images/kapibara.jpeg',
    'медоед': 'images/medoed.jpeg',
    'альпака': 'images/alpaka.jpeg',
    'малая панда': 'images/panda.jpeg',
    'сурикат': 'images/surikat.jpeg',
    'выдра': 'images/vqdra.jpeg',
    'пингвин': 'images/pingvin.jpeg',
    'морж': 'images/morz.jpeg'
}

QUESTIONS = [
    {
        'question' : '1. Когда вы наиболее работоспособны?',
        'answers' : {
            'Днём' : ['сурикат', 'морж', 'альпака', 'капибара', 'пингвин'],
            'Ночью' : ['медоед', 'малая панда', 'выдра']
        }
    },
    {
        'question' : '2.Что для вас важнее?',
        'answers' : {
            'Семья' : ['сурикат', 'выдра', 'альпака', 'капибара', 'морж', 'пингвин'],
            'Карьера' : ['медоед', 'малая панда']
        }
    },
    {
        'question' : '3. Без чего вы не можете обойтись в питании?',
        'answers' : {
            'Без мяса' : ['сурикат', 'медоед'],
            'Без овощей': ['капибара', 'альпака', 'малая панда' ],
            'Без Морепродуктов': ['морж', 'выдра', 'пингвин' ]

        }
    },
    {
        'question': '4. Какой цвет вам больше нравится?',
        'answers': {
            'Чёрный': ['медоед', 'пингвин'],
            'Оранжевый': ['малая панда', 'сурикат'],
            'Коричневый': ['капибара', 'альпака', 'выдра', 'морж']
        }
    },
    {
        'question': '5. Куда бы вы хотели отправиться в путешествие?',
        'answers': {
            'Арктика': ['морж', 'пингвин'],
            'Европа': ['выдра', 'альпака'],
            'Азия': ['малая панда', 'медоед'],
            'Африка': ['сурикат', 'капибара']
        }
    },
    {
        'question': '6. Что вы хотите от жизни?',
        'answers': {
            'Оставаться здоровым и сильным': ['медоед', 'морж'],
            'Никогда не скучать': ['выдра', 'сурикат'],
            'Известность и популярность': ['альпака', 'малая панда'],
            'Познать себя и мир вокруг': ['капибара', 'пингвин']
        }
    },
    {
        'question': '7. Вы купили новый шкаф. Чтобы собрать его, я...',
        'answers': {
            'обращусь к специалисту': ['капибара', 'пингвин', 'альпака', 'морж'],
            'найду дома инструменты ': ['выдра', 'медоед', 'малая панда', 'сурикат']
        }
    },
    {
        'question': '8. Вы бы хотели уметь: ',
        'answers': {
            'дышать под водой и хорошо плавать': ['выдра', 'морж', 'пингвин'],
            'быстро бегать и хорошо прятаться': ['сурикат', 'медоед'],
            'быть любимцем всех': ['капибара', 'альпака', 'малая панда']
        }
    },
    {
        'question': '9. Какое качество вы хотели бы в себе развить?',
        'answers': {
            'Стрессоустойчивость': ['медоед', 'морж'],
            'Бескорыстие': ['капибара', 'альпака'],
            'Общительность ': ['выдра', 'сурикат'],
            'Сила воли ': ['малая панда', 'пингвин']
        }
    }
    ]


COMMANDS = {
    '/start': 'начинает работу бота',
    '/help': 'показывает доступные команды бота',
    '/quiz': 'запускает викторину',
    '/care': 'ссылка на программу опеки',
    '/animals': 'список животных, о которых могу рассказать интересные факты',
    '/contact': 'связаться с сотрудником зоопарка',
    '/feedback': 'оставить отзыв',

}


class UserData:
    def __init__(self, user_id):
        self.user_id = user_id
        self.reset()

    def score(self, animals):
        for animal in animals:
            self.scores[animal] += 1

    def get_winner(self):
        return max(self.scores, key=self.scores.get)

    def reset(self):
        self.current_question = 0
        self.scores = {'капибара': 0,
                       'медоед': 0,
                       'альпака': 0,
                       'малая панда': 0,
                       'сурикат': 0,
                       'выдра': 0,
                       'пингвин' : 0,
                       'морж' : 0,
                       }



def get_animal_facts(animal):
    facts = []
    doc = docx.Document('info/animal_facts.docx')
    found = False
    for paragraph in doc.paragraphs:
         if paragraph.text.lower() == animal.lower() + ':':
             found = True
             continue
         if found:
             if paragraph.text.strip() =='':
                break
             facts.append(paragraph.text)
    return facts

def validate_animal(animal, available_animals):
    if animal not in available_animals:
        raise AnimalNotFoundException(animal)

def get_facts_text(animal, facts):
    if facts:
        return '\n \n'.join(facts[:3])
    else:
        return f'К сожалению, я не нашел фактов о животном {animal}'

