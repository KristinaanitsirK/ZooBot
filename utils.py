from config import get_facts_text
from extensions import AnimalNotFoundException

def send_animal_info(bot, chat_id, animal, image_path, facts):
    if image_path:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=f'Ваше тотемное животное: {animal}!')

    if facts:
        facts_text = get_facts_text(animal, facts)
        bot.send_message(chat_id, f'Вот три интересных факта о животном {animal}:\n\n{facts_text}')
    else:
        raise AnimalNotFoundException