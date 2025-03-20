import os
import re
import sys
import json
import datetime
import time
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
from bs4 import BeautifulSoup
import core as helper
from logs import logging
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, LOG, auth_users
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# YouTube Photo Download
photo = 'https://i.ibb.co/bgzZW56K/IMG-20250202-062354.jpg'

credit ="𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎" 
# Admin ID
ADMIN_ID = 5680454765
OWNER = int(os.environ.get("OWNER", 5680454765))
try: 
    ADMINS=[] 
    for x in (os.environ.get("ADMINS", "5680454765").split()):  
        ADMINS.append(int(x)) 
except ValueError: 
        raise Exception("Your Admins list does not contain valid integers.") 
ADMINS.append(OWNER)

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

OWNER = int(os.environ.get("OWNER", 5680454765))
failed_links = []  # List to store failed links
fail_cap =f"**➜ This file Contain Failed Downloads while Downloding \n You Can Retry them one more time **"

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await bot.polling()  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
    

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await asyncio.sleep(3600)  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
        
import random

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Nikhil_saini_khe"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/+3k-1zcJxINYwNGZl"),
        ],
    ]
)

# Inline keyboard for busy status
Busy = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Nikhil_saini_khe"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/+3k-1zcJxINYwNGZl"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://tinypic.host/images/2025/02/07/IMG_20250207_224444_975.jpg",
    "https://tinypic.host/images/2025/02/07/IMG_20250207_232047-1.jpg",
    "https://tinypic.host/images/2025/02/07/IMG_20250207_235607_759.jpg",
    "https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png",
    "https://tinypic.host/images/2025/02/07/IMG_20250208_002020.jpg",
    # Add more image URLs as needed
]

cookies_file_path = "youtube_cookies.txt"

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        # Replace the content of the target cookies file
        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")


# File paths
SUBSCRIPTION_FILE = "subscription_data.txt"

# Function to read subscription data
def read_subscription_data():
    if not os.path.exists(SUBSCRIPTION_FILE):
        return []
    with open(SUBSCRIPTION_FILE, "r") as f:
        return [line.strip().split(",") for line in f.readlines()]


# Function to write subscription data
def write_subscription_data(data):
    with open(SUBSCRIPTION_FILE, "w") as f:
        for user in data:
            f.write(",".join(user) + "\n")


# Admin-only decorator
def admin_only(func):
    async def wrapper(client, message: Message):
        if message.from_user.id != ADMIN_ID:
            await message.reply_text("You are not authorized to use this command.")
            return
        await func(client, message)
    return wrapper

@bot.on_message(filters.command(["logs"]) )
async def send_logs(bot: Client, m: Message):
    if m.chat.id not in auth_users:
        print(f"User ID not in auth_users", m.chat.id)
        await bot.send_message(m.chat.id, f"__**OOPS! You are not a Premium User.")
        return
        
    try:
        with open("logs.txt", "rb") as file:
            sent= await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete(True)
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")

@bot.on_message(filters.command(["adduser"]) & filters.private)
@admin_only
async def add_user(client, message: Message):
    try:
        _, user_id, expiration_date = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data.append([user_id, expiration_date])
        write_subscription_data(subscription_data)
        await message.reply_text(f"User {user_id} added with expiration date {expiration_date}.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /adduser [user_id] [expiration_date]")

@bot.on_message(filters.command(["removeuser"]) & filters.private)
@admin_only
async def remove_user(client, message: Message):
    try:
        _, user_id = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data = [user for user in subscription_data if user[0] != user_id]
        write_subscription_data(subscription_data)
        await message.reply_text(f"User {user_id} removed.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /removeuser [user_id]")


# Helper function to check admin privilege
def is_admin(user_id):
    return user_id == ADMIN_ID

# Command to show all users (Admin only)
@bot.on_message(filters.command("users") & filters.private)
async def show_users(client, message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    subscription_data = read_subscription_data()
    
    if subscription_data:
        users_list = "\n".join(
            [f"{idx + 1}. User ID: `{user[0]}`, Expiration Date: `{user[1]}`" for idx, user in enumerate(subscription_data)]
        )
        await message.reply_text(f"**👥 Current Subscribed Users:**\n\n{users_list}")
    else:
        await message.reply_text("ℹ️ No users found in the subscription data.")

@bot.on_message(filters.command(["myplan"]) & filters.private)
async def my_plan(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()  # Make sure this function is implemented elsewhere

    # Define YOUR_ADMIN_ID somewhere in your code
    if user_id == str(ADMIN_ID):  # YOUR_ADMIN_ID should be an integer
        await message.reply_text("**✨ 𝐘𝐎𝐔 𝐇𝐀𝐕𝐄 𝐋𝐈𝐅𝐄 𝐓𝐈𝐌𝐄 𝐀𝐂𝐂𝐄𝐒𝐒!**")
    elif any(user[0] == user_id for user in subscription_data):  # Assuming subscription_data is a list of [user_id, expiration_date]
        expiration_date = next(user[1] for user in subscription_data if user[0] == user_id)
        await message.reply_text(
            f"**📅 Your Premium Plan Status**\n\n"
            f"**🆔 User ID**: `{user_id}`\n"
            f"**⏳ Expiration Date**: `{expiration_date}`\n"
            f"**🔒 Status**: *Active*"
        )
    else:
        await message.reply_text("**❌ 𝓝𝓸 𝓼𝓾𝓫𝓼𝓬𝓻𝓲𝓹𝓽𝓲𝓸𝓷 𝓭𝓪𝓽𝓪 𝓯𝓸𝓾𝓷𝓭 𝓯𝓸𝓻 𝔂𝓸𝓾.**")
        
@bot.on_message(filters.command(["h2t"]))
async def add_channel(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the HTML file and its name
    await message.reply_text(
        "🎉 **Welcome to the HTML to Text Converter!**\n\n"
        "Please send your **HTML file** along with your desired **file name**! 📁\n\n"
        "Once you send the file, we'll process it and provide a neatly formatted text file for you! ✨"
    )

    try:
        # Wait for user to send HTML file
        input_message: Message = await bot.listen(message.chat.id)
        if not input_message.document:
            await message.reply_text(
                "🚨 **Error**: You need to send a valid **HTML file**. Please send a file with the `.html` extension."
            )
            return

        html_file_path = await input_message.download()

        # Ask the user for a custom file name
        await message.reply_text(
            "🔤 **Now, please provide the file name (without extension)**\n\n"
            "🔄**Please wait..5sec...⏳ for use default**"
        )

        # Wait for the custom file name input with a timeout of 5 seconds
        try:
            file_name_input: Message = await bot.listen(message.chat.id, timeout=5)
            custom_file_name = file_name_input.text.strip()
            await file_name_input.delete(True)
        except asyncio.TimeoutError:
            custom_file_name = "output"

        # If the user didn't provide a name, use the default one
        if not custom_file_name:
            custom_file_name = "output"
            
        await file_name_input.delete(True)

        # Process the HTML file and extract data
        with open(html_file_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            tables = soup.find_all('table')
            if not tables:
                await message.reply_text(
                    "🚨 **Error**: No tables found in the HTML file. Please ensure the HTML file contains valid data."
                )
                return

            videos = []
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:  # Ensure there's both a name and link
                        name = cols[0].get_text().strip()
                        link = cols[1].find('a')['href']
                        videos.append(f'{name}: {link}')

        # Create and send the .txt file with the custom name
        txt_file = os.path.splitext(html_file_path)[0] + f'_{custom_file_name}.txt'
        with open(txt_file, 'w') as f:
            f.write('\n'.join(videos))

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f"🎉 **Here is your neatly formatted text file**: `{custom_file_name}.txt`\n\n"
                    "You can now download and use the extracted content! 📥"
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

@bot.on_message(filters.command(["t2h"]))
async def txt_to_html(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the .txt file to convert to .html
    await message.reply_text(
        "🎉 **Welcome to the Text to HTML Converter!**\n\n"
        "Please send the **.txt file** you want to convert into an **.html** file.\n\n"
    )

    try:
        # Wait for the user to send the .txt file
        input_message: Message = await bot.listen(message.chat.id)
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await message.reply_text(
                "🚨 **Error**: Please send a valid **.txt file** to convert into an **.html** file."
            )
            return

        txt_file_path = await input_message.download()
        original_file_name = os.path.splitext(input_message.document.file_name)[0]

        # Ask the user for the custom file name
        await message.reply_text(
            f"🔤 **Now, please provide the file name (without extension)**\n\n"
            f"🔄**Please wait..5sec...⏳ for use default**\n\n"
            f"📔**Default Name** - {original_file_name}"
        )

        # Wait for the custom file name input with a timeout of 5 seconds
        try:
            file_name_input: Message = await bot.listen(message.chat.id, timeout=5)
            custom_file_name = file_name_input.text.strip()
            await file_name_input.delete(True)
        except asyncio.TimeoutError:
            custom_file_name = original_file_name

        # If the user didn't provide a name, use the original file name
        if not custom_file_name:
            custom_file_name = original_file_name

        # Read the contents of the .txt file
        with open(txt_file_path, 'r') as f:
            txt_content = f.readlines()

        # Convert the .txt content to HTML
        html_content = "<html>\n<body>\n"
        for line in txt_content:
            line = line.strip()
            if line.startswith("http"):
                html_content += f'<a href="{line}">CLICK HERE TO OPEN</a> - {line}<br/>\n'
            else:
                html_content += f"{line}<br/>\n"
        html_content += "</body>\n</html>"

        # Save the HTML content to a new file
        html_file_path = os.path.join("downloads", f"{custom_file_name}.html")
        os.makedirs(os.path.dirname(html_file_path), exist_ok=True)
        with open(html_file_path, 'w') as f:
            f.write(html_content)

        # Send the generated HTML file to the user with a pretty caption
        await message.reply_document(
            document=html_file_path,
            caption=f"🎉 **Here is your HTML file**: `{custom_file_name}.html`\n\n"
                    "You can now download and open it in your browser! 📥"
        )

        # Remove the temporary files after sending
        os.remove(txt_file_path)
        os.remove(html_file_path)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

@bot.on_message(filters.command(["t2t"]))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the text data and its desired file name
    await message.reply_text(
        "🎉 **Welcome to the Text to .txt Converter!**\n\n"
        "Please send the **text** you want to convert into a `.txt` file.\n\n"
    )

    try:
        # Wait for the user to send the text data
        input_message: Message = await bot.listen(message.chat.id)

        # Ensure the message contains text
        if not input_message.text:
            await message.reply_text(
                "🚨 **Error**: Please send valid text data to convert into a `.txt` file."
            )
            return

        text_data = input_message.text.strip()

        # Ask the user for the custom file name
        await message.reply_text(
            "🔤 **Now, please provide the file name (without extension)**\n\n"
            "🔄**Please wait..5sec...⏳ for use default**"
        )

        # Wait for the custom file name input with a timeout of 5 seconds
        try:
            inputn: Message = await bot.listen(message.chat.id, timeout=5)
            raw_textn = inputn.text
            await inputn.delete(True)
        except asyncio.TimeoutError:
            raw_textn = 'txt_file'

        if raw_textn == 'txt_file':
            custom_file_name = 'txt_file'
        else:
            custom_file_name = raw_textn

        # Create and save the .txt file with the custom name
        txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
        os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
        with open(txt_file, 'w') as f:
            f.write(text_data)

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f"🎉 **Here is your text file**: `{custom_file_name}.txt`\n\n"
                    "You can now download your content! 📥"
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'


@bot.on_message(filters.command(["e2t"]))
async def edit_txt(client, message: Message):
    user_id = str(message.from_user.id)
    # Prompt the user to upload the .txt file
    await message.reply_text(
        "🎉 **Welcome to the .txt File Editor!**\n\n"
        "Please send your `.txt` file containing subjects, links, and topics."
    )

    # Wait for the user to upload the file
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.document:
        await message.reply_text("🚨 **Error**: Please upload a valid `.txt` file.")
        return

    # Get the file name
    file_name = input_message.document.file_name.lower()

    # Define the path where the file will be saved
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file_name)

    # Download the file
    uploaded_file = await input_message.download(uploaded_file_path)

    # After uploading the file, prompt the user for the file name or 'd' for default
    await message.reply_text(
        "🔄 **Send your .txt file name, or type '/default' for the default file name.**"
    )

    # Wait for the user's response
    user_response: Message = await bot.listen(message.chat.id)
    if user_response.text:
        user_response_text = user_response.text.strip().lower()
        if user_response_text == '/default':
            # Handle default file name logic (e.g., use the original file name)
            final_file_name = file_name
        else:
            final_file_name = user_response_text + '.txt'
    else:
        final_file_name = file_name  # Default to the uploaded file name

    # Read and process the uploaded file
    try:
        with open(uploaded_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to read the file.\n\nDetails: {e}")
        return

    # Parse the content into subjects with links and topics
    subjects = {}
    current_subject = None
    for line in content:
        line = line.strip()
        if line and ":" in line:
            # Split the line by the first ":" to separate title and URL
            title, url = line.split(":", 1)
            title, url = title.strip(), url.strip()

            # Add the title and URL to the dictionary
            if title in subjects:
                subjects[title]["links"].append(url)
            else:
                subjects[title] = {"links": [url], "topics": []}

            # Set the current subject
            current_subject = title
        elif line.startswith("-") and current_subject:
            # Add topics under the current subject
            subjects[current_subject]["topics"].append(line.strip("- ").strip())

    # Sort the subjects alphabetically and topics within each subject
    sorted_subjects = sorted(subjects.items())
    for title, data in sorted_subjects:
        data["topics"].sort()

    # Save the edited file to the defined path with the final file name
    try:
        final_file_path = os.path.join(UPLOAD_FOLDER, final_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            for title, data in sorted_subjects:
                # Write title and its links
                for link in data["links"]:
                    f.write(f"{title}:{link}\n")
                # Write topics under the title
                for topic in data["topics"]:
                    f.write(f"- {topic}\n")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to write the edited file.\n\nDetails: {e}")
        return

    # Send the sorted and edited file back to the user
    try:
        await message.reply_document(
            document=final_file_path,
            caption="🎉 **Here is your edited .txt file with subjects, links, and topics sorted alphabetically!**"
        )
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to send the file.\n\nDetails: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)  



@bot.on_message(filters.command(["title"]))
async def run_bot(bot: Client, m: Message):
      editable = await m.reply_text("**Send Your TXT file with links**\n")
      input: Message = await bot.listen(editable.chat.id)
      txt_file = await input.download()
      await input.delete(True)
      await editable.delete()
      
      with open(txt_file, 'r') as f:
          lines = f.readlines()
      
      cleaned_lines = [line.replace('(', '').replace(')', '') for line in lines]
      
      cleaned_txt_file = os.path.splitext(txt_file)[0] + '_cleaned.txt'
      with open(cleaned_txt_file, 'w') as f:
          f.write(''.join(cleaned_lines))
      
      await m.reply_document(document=cleaned_txt_file,caption="Here is your cleaned txt file.")
      os.remove(cleaned_txt_file)

def process_links(links):
    processed_links = []
    
    for link in links.splitlines():
        if "m3u8" in link:
            processed_links.append(link)
        elif "mpd" in link:
            # Remove everything after and including '*'
            processed_links.append(re.sub(r'\*.*', '', link))
    
    return "\n".join(processed_links)

@bot.on_message(filters.command(["ytm"]))
async def txt_handler(bot: Client, m: Message):
    editable = await m.reply_text("🔹**Send me the TXT file containing YouTube links.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await bot.send_document(OWNER, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    await m.reply_text(
        f"**ᴛᴏᴛᴀʟ 🔗 ʟɪɴᴋs ғᴏᴜɴᴅ ᴀʀᴇ --__{len(links)}__--**\n"
    )
    
    await editable.edit("**🔹sᴇɴᴅ ғʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ**\n\n**🔹Please wait..10sec...⏳**\n\n**🔹For Download from Starting**")
    try:
        input0: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text = input0.text
        await input0.delete(True)
    except asyncio.TimeoutError:
        raw_text = '1'
        
        await editable.delete()
        try:
            arg = int(raw_text)
        except:
            arg = 1

    await m.reply_text(
        f"**⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ...⏳**\n"
    )
    
    count = int(raw_text)
    try:
        for i in range(arg-1, len(links)):  # Iterate over each link

            Vxy = links[i][1].replace("www.youtube-nocookie.com/embed", "youtu.be")
            url = "https://" + Vxy

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "")
            name = f'{name1[:60]} 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎'

            if "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp -x --audio-format mp3 --cookies {cookies_file_path} "{url}" -o "{name}.mp3"'
                print(f"Running command: {cmd}")
                os.system(cmd)
                if os.path.exists(f'{name}.mp3'):
                   print(f"File {name}.mp3 exists, attempting to send...")
                   try:
                       await bot.send_document(chat_id=m.chat.id, document=f'{name}.mp3', caption=f'**🎵 Title : **  {name}.mp3\n\n🔗**Video link** : {url}\n\n🌟** Extracted By** : 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎')
                       os.remove(f'{name}.mp3')
                   except Exception as e:
                       print(f"Error sending document: {str(e)}")
                else:
                     print(f"File {name}.mp3 does not exist.")                
    except Exception as e:
        await m.reply_text(f"🚨 **An error occurred**: {str(e)}")
    finally:
        await m.reply_text("🕊️Done Baby💞")

@bot.on_message(filters.command(["y2t"]))
async def youtube_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    
    await message.reply_text(
        "🎉 **Welcome to the YouTube to Text Converter!**\n\n"
        "Please send the **YouTube Channel, Playlist link** \n\n"
        "I convert into a `.txt` file.\n\n"
    )

    try:
        # Wait for the user to send the YouTube link
        input_message: Message = await bot.listen(message.chat.id, timeout=10)

        # Ensure the message contains a YouTube link
        if not input_message.text:
            await message.reply_text(
                "🚨 **Error**: Please send a valid YouTube link to convert into a `.txt` file."
            )
            return

        youtube_link = input_message.text.strip()

        # Fetch the YouTube information using yt-dlp with cookies
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'skip_download': True,
            'force_generic_extractor': True,
            'forcejson': True,
            'cookies': 'youtube_cookies.txt'  # Specify the cookies file
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(youtube_link, download=False)
                if 'entries' in result:
                    title = result.get('title', 'youtube_playlist')
                else:
                    title = result.get('title', 'youtube_video')
            except yt_dlp.utils.DownloadError as e:
                await message.reply_text(
                    f"🚨 **Error**: {str(e)}.\nPlease ensure the link is valid and try again."
                )
                return

        # Ask the user for the custom file name
        file_name_message = await message.reply_text(
            f"🔤 **Now, please provide the file name (without extension)**\n\n"
            f"If you're using default to **'{title}'**.\n\n"
            f"🔁...Please wait...10sec...⏳"
        )

        # Wait for the custom file name input with a timeout of 10 seconds
        try:
            file_name_input: Message = await bot.listen(message.chat.id, timeout=10)
            custom_file_name = file_name_input.text.strip()
            await file_name_input.delete(True)
        except asyncio.TimeoutError:
            custom_file_name = title

        # If the user didn't provide a name, use the default one
        if not custom_file_name:
            custom_file_name = title

        await file_name_message.delete(True)

        # Extract the YouTube links
        videos = []
        if 'entries' in result:
            for entry in result['entries']:
                video_title = entry.get('title', 'No title')
                url = entry['url']
                videos.append(f"{video_title}: {url}")
        else:
            video_title = result.get('title', 'No title')
            url = result['url']
            videos.append(f"{video_title}: {url}")

        # Create and save the .txt file with the custom name
        txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
        os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
        with open(txt_file, 'w') as f:
            f.write('\n'.join(videos))

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f"🎉 **Here is your YouTube links text file**: `{custom_file_name}.txt`\n\n"
                    "You can now download your content! 📥"
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
            )

@bot.on_message(filters.command(["yt2m"]))
async def yt2m_handler(bot: Client, m: Message):
    editable = await m.reply_text(f"🔹**Send me the YouTube link**\n")
    input: Message = await bot.listen(editable.chat.id)
    youtube_link = input.text.strip()
    await input.delete(True)

    Show = f"**⚡Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ...⏳**\n\n🔗𝐔𝐑𝐋 »  {youtube_link}\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ 🇸‌🇦‌🇮‌🇳‌🇮‌🐦"
    await editable.edit(Show, disable_web_page_preview=True)
    await asyncio.sleep(10)

    try:
        Vxy = youtube_link.replace("www.youtube-nocookie.com/embed", "youtu.be")
        url = Vxy

        # Fetch the YouTube video title using oEmbed
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        response = requests.get(oembed_url)
        audio_title = response.json().get('title', 'YouTube Video')

        name = f'{audio_title[:60]} 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎'
        
        if "youtube.com" in url or "youtu.be" in url:
            cmd = f'yt-dlp -x --audio-format mp3 --cookies {cookies_file_path} "{url}" -o "{name}.mp3"'
            print(f"Running command: {cmd}")
            os.system(cmd)
            if os.path.exists(f'{name}.mp3'):
                print(f"File {name}.mp3 exists, attempting to send...")
                try:
                    await editable.delete()
                    await bot.send_document(chat_id=m.chat.id, document=f'{name}.mp3', caption=f'**🎵 Title : **  {name}.mp3\n\n🔗**Video link** : {url}\n\n🌟** Extracted By** : 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎')
                    os.remove(f'{name}.mp3')
                except Exception as e:
                    print(f"Error sending document: {str(e)}")
            else:
                print(f"File {name}.mp3 does not exist.")
    except Exception as e:
        await m.reply_text(f"🚨 **An error occurred**: {str(e)}")
        
@bot.on_message(filters.command(["help"]))
async def txt_handler(client: Client, m: Message):
    await bot.send_message(m.chat.id, text= (
        " 🎉**Congrats! You are using 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎**:\n\n"
        "01. Send /start - To Check Bot \n\n"
        "02. Send /yt2m - YT mp3 Downloader by link \n\n"
        "03. Send /ytm - YT mp3 Downloader by .txt \n\n"
        "04. Send /y2t - YouTube to .txt Convert\n\n"
        "05. Send /link - link downloader\n\n"
        "06. Send /doc- Pdf & jpg downloader\n\n"
        "07. Send /id - Your Telegram ID\n\n"
        "08. Send /info - Your Telegram Info\n\n"
        "09. Send /h2t - HTML to .txt Convert\n\n"
        "10. Send /e2t - Txt in Alphabetically\n\n"
        "11. Send /t2t - Text to .txt Convert\n\n"
        "12. Send /title - Title Clean from Symbol\n\n"
        "13. Send /adduser - For authorisation user\n\n"
        "14. Send /removeuser - For remove authorised user\n\n"
        "15. Send /users - To see authorised user\n\n"
        "16. Send /myplan - To see your plan\n\n"
        "17. Send /stop - Stop the Running Task. 🚫\n\n"
        "If you have any questions, feel free to ask! 💬"
)
                          )
    
@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, m: Message):
    
    text = f"""**———✦Information✦———**

**🙋🏻‍♂️ Your Name :** {m.from_user.first_name} {m.from_user.last_name if m.from_user.last_name else 'None'}
**🧑🏻‍🎓 Your Username :** @{m.from_user.username}
**🆔 Your Telegram ID :** {m.from_user.id}
**🔗 Your Profile Link :** {m.from_user.mention}"""
    
    await m.reply_text(        
        text=text,
        disable_web_page_preview=True,
    )


@bot.on_message(filters.private & filters.command(["id"]))
async def id(bot: Client, update: Message):
    if update.chat.type == "channel":
        await update.reply_text(
            text=f"**This Channel's ID:** {update.chat.id}",
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(        
            text=f"**Your Telegram ID :** {update.from_user.id}",
            disable_web_page_preview=True,
        )  

# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    # Send a loading message
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Loading... ⏳🔄"
    )
  
    # Choose a random image URL
    random_image_url = random.choice(image_urls)
    
    # Caption for the image
    caption = (
        "🌟 Welcome {0}! 🌟\n\n"
        "Checking status Ok... \nFor command **ᴊᴏɪɴ ᴏᴜʀ <a href='https://t.me/+1e-r94cF6yE3NzA1'>__TG Channel__</a>**\n**Add me in <a href='http://t.me/nklmultiforward_bot?startchannel=true'>__Your Channel__</a>**\n**Add me in <a href='http://t.me/nklmultiforward_bot?startgroup=true'>__Your Group__</a>**\n**Send /help for any Help...**"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Initializing Uploader bot... 🤖\n\n"
        "Progress: ⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Loading features... ⏳\n\n"
        "Progress: 🟥🟥⬜⬜⬜⬜⬜⬜ 25%\n\n"
    )
    
    await asyncio.sleep(1)
    await loading_message.edit_text(
        "This may take a moment, sit back and relax! 😊\n\n"
        "Progress: 🟧🟧🟧🟧⬜⬜⬜⬜ 50%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Checking Bot Status... 🔍\n\n"
        "Progress: 🟨🟨🟨🟨🟨🟨⬜⬜ 75%\n\n"
    )

    await asyncio.sleep(1)
    await loading_message.edit_text(
        "Checking status Ok... \nFor command **ᴊᴏɪɴ ᴏᴜʀ <a href='https://t.me/+1e-r94cF6yE3NzA1'>ᴛᴇʟᴇɢʀᴀᴍ Group</a>**\n\n"
        "Progress:🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n\n"
    )
        
    # Send the image with caption and buttons
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption.format(message.from_user.mention),
        reply_markup=keyboard
    )

    # Delete the loading message
    await loading_message.delete()


@bot.on_message(filters.command(["stop"]))
async def restart_handler(_, m):
    
        if failed_links:
         error_file_send = await m.reply_text("**📤 Sending your Failed Downloads List Before Stoping   **")
         with open("failed_downloads.txt", "w") as f:
          for link in failed_links:
            f.write(link + "\n")
    # After writing to the file, send it
         await m.reply_document(document="failed_downloads.txt", caption=fail_cap)
         await error_file_send.delete()
         os.remove(f'failed_downloads.txt')
         failed_links.clear()
         processing_request = False  # Reset the processing flag
         await m.reply_text("🚦**ˢᵗᵒᵖᵖᵉᵈ ᵇᵃᵇʸ**🚦", True)
         os.execl(sys.executable, sys.executable, *sys.argv)
        else:
         processing_request = False  # Reset the processing flag
         await m.reply_text("🚦**ˢᵗᵒᵖᵖᵉᵈ ᵇᵃᵇʸ**🚦", True)
         os.execl(sys.executable, sys.executable, *sys.argv)
   

@bot.on_message(filters.command(["saini"]) )
async def txt_handler(bot: Client, m: Message):
    if m.chat.id not in auth_users:
        print(f"User ID not in auth_users", m.chat.id)
        await bot.send_message(m.chat.id, f"__**OOPS! You are not a Premium User.")
        return
    editable = await m.reply_text(f"**🔹Hi I am Poweful TXT Downloader📥 Bot.**\n🔹**Send me the TXT file and wait.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await bot.send_document(OWNER, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎"
    pw_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDIxODc2NTcuNTQ0LCJkYXRhIjp7Il9pZCI6IjYyZmEzM2UxYTliZTQ1MDAxMWY1OWYyYSIsInVzZXJuYW1lIjoiOTA2MDYwOTYzOSIsImZpcnN0TmFtZSI6InNhdHlhbSIsImxhc3ROYW1lIjoic2luZ2giLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sInR5cGUiOiJVU0VSIn0sImlhdCI6MTc0MTU4Mjg1N30.lDii_Ou4JtXTCqRCv0E70ShJr2vj_9UYmsanVZU7hec"
    await editable.edit(f"**⚙️Pocessing Input.......**")
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("🔹invalid file input.")
        os.remove(x)
        return
 
    await editable.edit(f"🔹Total 🔗 links found are __**{len(links)}**__\n\n🔹Send From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    if int(input0.text) > len(links) :
        await editable.edit(f"**🔹Error : Enter number in range of Index**")
        processing_request = False  # Reset the processing flag
        await m.reply_text("**🔹Exiting Task......  **")
        return
    else: await input0.delete(True)

    try:
        arg = int(raw_text)
    except:
        arg = 1

    await editable.edit(f"**🔹Enter till where you want to download**\n\n**🔹Starting Dowload Form : `{raw_text}`\n🔹Last Index of Links is : `{len(links)}` **")
    input9: Message = await bot.listen(editable.chat.id)
    raw_text9 = input9.text
    
    if int(input9.text) > len(links) :
        await editable.edit(f"**🔹Error : Enter number in range of Index**")
        processing_request = False  # Reset the processing flag
        await m.reply_text("**🔹Exiting Task......  **")
        return
    else: await input9.delete(True)
        
    await editable.edit(f"**🔹Enter Batch Name**\n\n**🔹Please wait...10sec...⏳ for use**\n\n🔹𝐍𝐚𝐦𝐞 » __**{file_name}__**")
    try:
        input1: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text0 = input1.text
        await input1.delete(True)
    except asyncio.TimeoutError:
        raw_text0 = '/default'
    
    if raw_text0 == '/default':
        b_name = file_name
    else:
        b_name = raw_text0
        
    await editable.edit("**╭━━━━❰ᴇɴᴛᴇʀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ❱━➣\n┣━━⪼ 🔹sᴇɴᴅ **144** for  144p\n┣━━⪼ 🔹sᴇɴᴅ **240** for  240p\n┣━━⪼ 🔹sᴇɴᴅ **360** for  360p\n┣━━⪼ 🔹sᴇɴᴅ **480** for  480p\n┣━━⪼ 🔹sᴇɴᴅ **720** for  720p\n┣━━⪼ 🔹sᴇɴᴅ **1080** for 1080p\n╰━━⌈⚡[🦋🇸‌🇦‌🇮‌🇳‌🇮‌🦋]⚡⌋━━➣ **")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**🔹Enter Your Name**\n\n**🔹Please wait..10sec...⏳ for use default**")
    try:
        input3: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text3 = input3.text
        await input3.delete(True)
    except asyncio.TimeoutError:
        raw_text3 = '/admin'

    # Default credit message
    credit = "️𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🕊️⁪⁬⁮⁮⁮"
    if raw_text3 == '/admin':
        CR = '𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🕊️'
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
        
    await editable.edit("**🔹Enter Working **PW Token** For 𝐌𝐏𝐃 𝐔𝐑𝐋**\n**🔹Please wait..5sec...⏳ for use default**")
    try:
        input4: Message = await bot.listen(editable.chat.id, timeout=5)
        raw_text4 = input4.text
        await input4.delete(True)
    except asyncio.TimeoutError:
        raw_text4 = '/pw'
    
    if raw_text4 == '/pw':
        PW = pw_token
    else:
        PW = raw_text4
        
    await editable.edit("🔹Send   ☞ **no** for **video** format\n\n🔹Send   ☞ **No** for **Document** format\n\n**🔹Please wait..5sec...⏳ for use default**")
    try:
        input6: Message = await bot.listen(editable.chat.id, timeout=5)
        raw_text6 = input6.text
        await input6.delete(True)
    except asyncio.TimeoutError:
        raw_text6 = 'no'
    
    await editable.delete()
    
    thumb = raw_text6
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"
        
    await bot.send_message(chat_id=m.chat.id, text=f"__**🎯Target Batch :  {b_name} **__")

    count =int(raw_text)    
    try:
        for i in range(arg-1, int(input9.text)):
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']
                            
            elif '/master.mpd' in url:
             vid_id =  url.split("/")[-2]
             url =  f"https://madxapi-d0cbf6ac738c.herokuapp.com/{vid_id}/master.m3u8?token={PW}"
                
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]}'
            
            if 'cpvod.testbook.com' in url:
               url = requests.get(f'https://mon-key-3612a8154345.herokuapp.com/get_keys?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ0Mjg3MzI5LCJvcmdJZCI6MTM5MzQsInR5cGUiOjEsIm1vYmlsZSI6IjkxNzA3OTgyMzkxOSIsIm5hbWUiOiJuYW1lIiwiZW1haWwiOiJkZmI1OThmMDZiMmQ0MDFmYmVmZjU3YTI5ZTJlMjBhMkBnbWFpbC5jb20iLCJpc0ludGVybmF0aW9uYWwiOjAsImRlZmF1bHRMYW5ndWFnZSI6IkVOIiwiY291bnRyeUNvZGUiOiJJTiIsImNvdW50cnlJU08iOiI5MSIsInRpbWV6b25lIjoiR01UKzU6MzAiLCJpc0RpeSI6dHJ1ZSwib3JnQ29kZSI6InprcXBlIiwiaXNEaXlTdWJhZG1pbiI6MCwiZmluZ2VycHJpbnRJZCI6IjQyMGFhY2RiYTQzY2Y0M2RkYjY1MGI4NzllZGRiNzdlYzc4ZTVkNzNmMDJmMzBkNmVhYjNlNDVhOTY4OGIyM2YiLCJpYXQiOjE3Mzk4NTI5OTAsImV4cCI6MTc0MDQ1Nzc5MH0.e2z_nUORHv0IZAhEEBs3eV30Hz7L19juGL5Dwo8hPZdL7VoL0ujfg5zF1RtW5PxR'}).json()['url']
                   
            if "/master.mpd" in url :
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/","https://d1d34p8vz63oiq.cloudfront.net/")
                    print(url)
                else: 
                    url = url    

                print("mpd check")
                key = await helper.get_drm_keys(url)
                print(key)
                await m.reply_text(f"got keys form api : \n`{key}`")
          
            if "/master.mpd" in url:
                cmd= f" yt-dlp -k --allow-unplayable-formats -f bestvideo.{quality} --fixup never {url} "
                print("counted")

            

            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov
                
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n**🎞️ Title : **  {name1} [{res}].mp4\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**'
                cc1 = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n**📁 Title : **  {name1} .pdf\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**'
                cczip = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n**📁 Title : **  {name1} .zip\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**'
                ccimg = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n**📁 Title : **  {name1} .jpg\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**' 
                ccyt = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n**🎞️ Title : ** : {name1} .mkv\n**├── Resolution :** [{res}]\n**├── Video link :** {url}\n\n**📚 Course : ** : {b_name}\n\n**🌟 Extracted By : {CR}**'
                ccm = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n**🎵 Title : **  {name1} .mp3\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**' 
             
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count+=1
                        continue

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue      
                        
                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=ccm)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.{ext}', caption=ccimg)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue
                                
                else:
                    Show = f"**⚡Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ...⏳**\n\n📚𝐓𝐢𝐭𝐥𝐞 » `{name}\n\n🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {raw_text2}p`\n\n🔗𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐥𝐢𝐧𝐤 » {count}\n\n🖇️𝐓𝐨𝐭𝐚𝐥 𝐥𝐢𝐧𝐤𝐬 » {len(links)}\n\n🌿𝐔𝐑𝐋 »  {url}\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ 🇸‌🇦‌🇮‌🇳‌🇮‌🐦"
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                    Error= f"⚠️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n⚠️ 𝐍𝐚𝐦𝐞 » {name}\n⚠️ 𝐔𝐑𝐋 »  {url}\n\n"
                    await m.reply_text(Error, disable_web_page_preview=True)
                    failed_links.append(f"{name1} : {url}")
                    count += 1
                    continue

    except Exception as e:
        await m.reply_text(e)
    time.sleep(2)

    if failed_links:
     error_file_send = await m.reply_text("**📤 Sending you Failed Downloads List **")
     with open("failed_downloads.txt", "w") as f:
        for link in failed_links:
            f.write(link + "\n")
    # After writing to the file, send it
     await m.reply_document(document="failed_downloads.txt", caption=fail_cap)
     await error_file_send.delete()
     failed_links.clear()
     os.remove(f'failed_downloads.txt')
    await m.reply_text("🕊️Done Baby💞")
    
@bot.on_message(filters.command(["doc"]) )
async def txt_handler(bot: Client, m: Message):
    editable = await m.reply_text(f"**🔹Hi I am TXT to Doc Downloader📥 Bot.**\n🔹**Send me the TXT file and wait.**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await bot.send_document(OWNER, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎"
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return
   
    await editable.edit(f"🔹Total 🔗 links found are __**{len(links)}**__\n\n🔹Send From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1
    await editable.edit(f"**🔹Enter Batch Name**\n\n**🔹Please wait...10sec...⏳ for use**\n\n🔹𝐍𝐚𝐦𝐞 » __**{file_name}__**")
    try:
        input1: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text0 = input1.text
        await input1.delete(True)
    except asyncio.TimeoutError:
        raw_text0 = '/default'
    
    if raw_text0 == '/default':
        b_name = file_name
    else:
        b_name = raw_text0
    
    await editable.edit("**🔹Enter Your Name**\n\n**🔹Please wait..10sec...⏳ for use default**")
    try:
        input3: Message = await bot.listen(editable.chat.id, timeout=10)
        raw_text3 = input3.text
        await input3.delete(True)
    except asyncio.TimeoutError:
        raw_text3 = '/admin'

    # Default credit message
    credit = "️𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🕊️⁪⁬⁮⁮⁮"
    if raw_text3 == '/admin':
        CR = '𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎 🕊️'
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
        
    await editable.delete()
    await m.reply_text(
        f"__**🎯Target Batch :  {b_name} **__"
    )

    count =int(raw_text)    
    try:
        for i in range(arg-1, len(links)):
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]} 𝙎𝘼𝙄𝙉𝙄 𝘽𝙊𝙏𝙎'

            try:  
                cc1 = f'**[📕]Pdf Id  ➠** {str(count).zfill(3)}\n**[📁]Tᴏᴘɪᴄ ➠** {name1} .pdf\n\n<pre><code>**📚 Course ➠** {b_name}</code></pre>\n\n** 🌟 Extracted By : {CR}**'                 
                ccimg = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n** Title : **  {name1} .jpg\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**' 
                ccm = f'**——— ✦  {str(count).zfill(3)} ✦ ———**\n\n**🎵 Title : **  {name1} .mp3\n\n<pre><code>**📚 Course :** {b_name}</code></pre>\n\n**🌟 Extracted By : {CR}**' 
            
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count+=1
                        pass

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=ccm)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        pass

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.{ext}', caption=ccimg)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        pass
                                
            except Exception as e:
                    Error= f"⚠️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n"
                    await m.reply_text(Error, disable_web_page_preview=True)
                    count += 1
                    pass

    except Exception as e:
        await m.reply_text(e)
   

bot.run()
if __name__ == "__main__":
    asyncio.run(main())
