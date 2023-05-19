import os
import re
import random

def convert_media(message, media_dir):
    media = re.search(r'(\(\w+ (omessi|file non presente)\))|(\w+(?:-\w+)*\.(opus|webp|jpg|mp4))', message)
    if media:
        media = media.group()
        if media.endswith(('webp', 'jpg', 'mp4')):
            return f'<br><img src="{os.path.join(media_dir, media)}" width="200"><br>'
        elif media.endswith('opus'):
            return f'<audio controls><source src="{os.path.join(media_dir, media)}" type="audio/ogg"></audio><br>'
        elif 'file non presente' in media:
            return f'<div style="background-color: rgb(64, 65, 78); border-radius: 10px; padding: 5px; text-align: left; display: inline-block;">File non presente ({media})</div><br>'
    return ''

def generate_html(chat_file, title, user_name):
    media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
    participants = set()
    participant_colors = {}  # Mappa per memorizzare i colori dei partecipanti
    messages = []

    with open(chat_file, 'r', encoding='utf-8') as file:
        current_date = None
        for line in file:
            line = line.strip()
            if line:
                message_match = re.search(r'(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}) - (.*?): (.*)', line)
                if message_match:
                    date, time, sender, content = message_match.groups()
                    participants.add(sender)

                    if sender not in participant_colors:
                        # Assegna un colore casuale al partecipante
                        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        participant_colors[sender] = f'rgb{rgb}'

                    color = participant_colors[sender]

                    if current_date != date:
                        current_date = date
                        date_html = f'<div class="date" style="text-align: center; background-color: rgb(33, 33, 33); border-radius: 10px; padding: 5px; margin-bottom: 10px;">{date}</div>'
                        messages.append(date_html)

                    if sender == user_name:
                        align = 'right'
                        sender_html = f'<strong><span style="color: {color};">{sender}</span> - <span style="color: white;">{time}</span></strong>'
                    else:
                        align = 'left'
                        sender_html = f'<strong><span style="color: {color};">{sender}</span> - <span style="color: white;">{time}</span></strong>'

                    media_html = convert_media(content, media_dir)
                    content = content.replace('(file allegato)', '').strip()
                    content = media_html if media_html else content

                    message_html = f'<div class="message" style="text-align: {align};">'
                    message_html += f'<div class="content" style="background-color: rgb(64, 65, 78); border-radius: 10px; padding: 5px;">'
                    message_html += f'{sender_html}<br>{content}'
                    message_html += f'</div></div>'
                    messages.append(message_html)

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{
                background-image: url('wallpaper.png');
                background-repeat: no-repeat;
                background-size: cover;
                background-position: center;
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
                color: #ffffff;
                zoom: 125%;
            }}

            .container {{
                margin: 0 auto;
                padding: 10px;
                background-color: transparent;
            }}

            .messages {{
                overflow-y: scroll;
                height: 600px;
                padding: 10px;
            }}

            .message {{
                margin-bottom: 10px;
            }}

            .content {{
                background-color: rgb(64, 65, 78);
                border-radius: 10px;
                padding: 5px;
                display: inline-block;
            }}

            .date {{
                text-align: center;
                margin-top: 20px;
                font-weight: bold;
                background-color: rgb(33, 33, 33);
                border-radius: 10px;
                padding: 5px;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <div class="messages">
                {"".join(messages)}
            </div>
        </div>
    </body>
    </html>
    '''

    return html

chat_file = 'chat.txt'
title = input("Inserisci il titolo della chat (premere Invio per usare il valore predefinito 'Chat WhatsApp'): ") or 'Chat WhatsApp'
user_name = input("Inserisci il tuo nome: ")

html = generate_html(chat_file, title, user_name)

with open('chat.html', 'w', encoding='utf-8') as file:
    file.write(html)
