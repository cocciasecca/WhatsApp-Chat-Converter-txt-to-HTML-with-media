import os
import re
import random

def convert_media(message, media_dir, platform):
    if platform == 'i':
        media = re.search(r'<allegato: (.*?)>', message)
    elif platform == 'a':
        media = re.search(r'(\(\w+ (omessi|file non presente)\))|(\w+(?:-\w+)*\.(opus|webp|jpg|mp4|3gp))', message)
    else:
        media = None

    if media:
        media = media.group(1) if platform == 'i' else media.group()
        if media == '<Media omessi>':
            return '*Media omessi*<br>'
        if media.endswith(('webp', 'jpg')):
            return f'<br><img src="./media/{media}" width="200"><br>'
        elif media.endswith(('mp4', '3gp')):
            return f'<br><video width="200" controls><source src="./media/{media}" type="video/{media[-3:]}"></video><br>'
        elif media.endswith('opus'):
            return f'<audio controls><source src="./media/{media}" type="audio/ogg"></audio><br>'
        else:
            return f'<div style="background-color: rgb(64, 65, 78); border-radius: 10px; padding: 5px; text-align: left; display: inline-block;">File non presente ({media})</div><br>'
    return ''

def generate_html(chat_file, title, user_name, platform, date_format):
    media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
    participants = set()
    participant_colors = {}
    messages = []

    with open(chat_file, 'r', encoding='utf-8') as file:
        current_date = None
        previous_line_was_message = False
        for line in file:
            line = line.strip()
            if line:
                if platform == 'a':
                    if date_format == '1':
                        message_match = re.search(r'(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}) - (.*?)(?=:|$)(?:: )?(.*)', line)
                    elif date_format == '2':
                        message_match = re.search(r'(\d{2}.\d{2}.\d{2}), (\d{2}:\d{2}) - (.*?)(?=:|$)(?:: )?(.*)', line)
                elif platform == 'i':
                    message_match = re.search(r'\[(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}):\d{2}\] (.*?)(?=:|$)(?:: )?(.*)', line)
                else:
                    message_match = None

                if message_match:
                    date, time, sender, content = message_match.groups()
                    participants.add(sender)

                    if sender not in participant_colors:
                        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        participant_colors[sender] = f'rgb{rgb}'

                    color = participant_colors[sender]

                    if current_date != date:
                        current_date = date
                        date_html = f'<div class="date" style="text-align: center; background-color: rgb(33, 33, 33); border-radius: 10px; padding: 5px; margin-bottom: 10px;">{date}</div>'
                        messages.append(date_html)

                    if content == '' and platform == 'a': # General group message on Android
                        align = 'center'
                        sender_html = f'<strong><span style="color: white;">{sender}</span></strong>'
                    elif sender == title and platform == 'i': # General group message on iOS
                        align = 'center'
                        sender_html = f'<strong><span style="color: white;">{content}</span></strong>'
                    elif sender == user_name:
                        align = 'right'
                        sender_html = f'<strong><span style="color: {color};">{sender}</span> - <span style="color: white;">{time}</span></strong>'
                    else:
                        align = 'left'
                        sender_html = f'<strong><span style="color: {color};">{sender}</span> - <span style="color: white;">{time}</span></strong>'

                    media_html = convert_media(content, media_dir, platform)
                    if media_html:
                        content = media_html
                    elif content == '<Media omessi>':
                        content = '*Media omessi*'

                    message_html = f'<div class="message" style="text-align: {align};">'
                    message_html += f'<div class="content" style="background-color: rgb(64, 65, 78); border-radius: 10px; padding: 5px;">'
                    if sender == title:
                        message_html += f'{sender_html}'
                    else:
                        message_html += f'{sender_html}<br>{content}'
                    message_html += f'</div></div>'
                    messages.append(message_html)

                    previous_line_was_message = True
                else:
                    if previous_line_was_message:
                        messages[-1] = messages[-1].replace('</div></div>', f'<br>{line}</div></div>')
                    else:
                        previous_line_was_message = False

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

run_program = 1
platform = input("Was the chat exported from Android or iOS? (A/i): ").strip().lower()

if os.path.exists('chat.txt'):
    chat_file = 'chat.txt'
elif os.path.exists('_chat.txt'):
    chat_file = '_chat.txt'
else:
    run_program = 0
    print("Neither 'chat.txt' nor '_chat.txt' was found.")

if run_program:
    print("1:    25/06/24, 21:10 - Person 1: Hello\n2:    01.10.20, 11:03 - Person 1: Hello")
    date_format = input("Which of these two examples looks more like your chat txt file (1/2)? ").strip()
    title = input("Enter the chat title (or press Enter to use the default value 'WhatsApp Chat'): ") or 'Chat WhatsApp'
    user_name = input("Enter your chat name: ")

    html = generate_html(chat_file, title, user_name, platform, date_format)

    with open('chat.html', 'w', encoding='utf-8') as file:
        file.write(html)
