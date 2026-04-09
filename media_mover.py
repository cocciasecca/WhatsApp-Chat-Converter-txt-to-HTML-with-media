import os
import re

run_program = 1

def extract_media(chat_file, media_list_file, platform):
    media_list = []

    with open(chat_file, 'r', encoding='utf-8') as file:
        for line in file:
            
            if platform == 'i':  # iOS
                media_match = re.search(
                    r'<allegato:\s*([^>]+)>|(\(\w+ (?:omessi|file non presente)\))',
                    line
                )
                if media_match:
                    media = media_match.group(1) or media_match.group(2)
                    media_list.append(media)

            else:  # Android (default)
                media_match = re.search(
                    r'(\(\w+ (?:omessi|file non presente)\))|(\w+(?:-\w+)*\.(?:opus|webp|jpg|jpeg|png|gif|mp4|vcf|csv))',
                    line
                )
                if media_match:
                    media = media_match.group(1) or media_match.group(2)
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





if os.path.exists('chat.txt'):
    chat_file = 'chat.txt'
elif os.path.exists('_chat.txt'):
    chat_file = '_chat.txt'
else:
    run_program = 0
    print("Neither 'chat.txt' nor '_chat.txt' was found.")


if run_program:
    platform = input("Was the chat exported from Android or iOS? (A/i): ").strip().lower()

    if platform not in ['a', 'i']:
        print("Invalid input. Defaulting to Android.")
        platform = 'a'

    media_list_file = 'media_list.txt'
    print("Created media list txt file.")
    
    extract_media(chat_file, media_list_file, platform)
    
    media_dir = 'media'
    move_media(media_list_file, media_dir)
    
    respond = input("Do you want to keep the media_list.txt file? (Y/N): ").strip().lower()
    if respond == 'n':
        os.remove("media_list.txt")
