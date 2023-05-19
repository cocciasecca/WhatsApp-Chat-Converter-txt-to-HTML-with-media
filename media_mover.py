import os

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

media_list_file = 'media_list.txt'
media_dir = 'media'

move_media(media_list_file, media_dir)
