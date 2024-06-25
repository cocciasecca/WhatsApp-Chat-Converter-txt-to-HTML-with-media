# WhatsApp Chat Converter ![image](https://web.whatsapp.com/favicon-64x64.ico)

Are you tired of dealing with the hassle of converting your old WhatsApp chats into a more readable format? I mean, who wants to keep those cluttered and unreadable TXT exports, right? Well, fret no more! We have the perfect solution for you: an amazing tool crafted with the assistance of Chat-GPT.

With this tool, you can effortlessly convert your TXT files, along with all the media, into sleek and easily digestible HTML format. Say goodbye to the headache of deciphering messy TXT exports and hello to organized and visually appealing chat history. It's like waving a magic wand and transforming chaos into order!

Give it a shot! Embrace the freedom of deleting those old chats from WhatsApp while still preserving your memories in a neat and accessible format. This tool is a real game-changer, designed to make your life simpler. So why wait? Experience the convenience and efficiency of converting your chats to HTML with just a few clicks.

## Getting Started

### Prerequisites
Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Instructions
1. **Clone the repository and navigate to the cloned directory.**
    ```bash
    git clone https://github.com/yourusername/whatsapp-chat-converter.git
    cd whatsapp-chat-converter
    ```
2. **Move the chat text file into the same folder as the script and make sure it's named `chat.txt` or `_chat.txt`.**
3. **Download the WhatsApp background image** from the following URL: [WhatsApp Background Image](https://i.pinimg.com/originals/97/c0/07/97c00759d90d786d9b6096d274ad3e07.png).
4. **Place the downloaded image in the same folder as the script and rename it as `wallpaper.png`.**
5. **Move all the media files** referenced in the chat into a folder named `media` in the same folder as the script. You can do this manually or using the `media_mover` script (which will automatically create a `media` folder).
    ```bash
    python3 media_mover.py
    ```
6. **Execute the script** by running the following command in the terminal:
    ```bash
    python3 whatsapp_txt_to_html.py
    ```

## 📋 FAQ

### ❓ Why are some characters like 'à' or 'é' not displayed correctly on the first page loading?
Try to refresh the page one or two times. In some languages, certain characters may not display correctly on the initial page load. Refreshing the page usually resolves this issue and ensures all characters are displayed properly.
