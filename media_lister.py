import re

def extract_media(chat_file, media_list_file):
    media_list = []

    with open(chat_file, 'r', encoding='utf-8') as file:
        for line in file:
            media_match = re.search(r'(\(\w+ (?:omessi|file non presente)\))|(\w+(?:-\w+)*\.(?:opus|webp|jpg|mp4))', line)
            if media_match:
                media = media_match.group()
                media_list.append(media)

    with open(media_list_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(media_list))

chat_file = 'chat.txt'
media_list_file = 'media_list.txt'

extract_media(chat_file, media_list_file)
