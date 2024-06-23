import os
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

def move_media(media_list_file, media_dir):
    with open(media_list_file, 'r', encoding='utf-8') as file:
        media_list = file.read().splitlines()

    if not os.path.exists(media_dir):
        os.mkdir(media_dir)

    for media in media_list:
        if os.path.exists(media):
            new_path = os.path.join(media_dir, os.path.basename(media))
            os.rename(media, new_path)
            print(f"Moved '{media}' to '{new_path}'")
        else:
            print(f"File '{media}' not found.")

chat_file = 'chat.txt'
media_list_file = 'media_list.txt'
print("Created media list txt file.")

extract_media(chat_file, media_list_file)

media_dir = 'media'
move_media(media_list_file, media_dir)

respond = input("Do you want to keep the media_list.txt file, with all the media listed?(Y/N): ").strip().lower()
if respond == 'n':
    os.remove("media_list.txt")
