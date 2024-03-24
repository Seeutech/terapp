import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN
import re

# Initialize the Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define a handler for the /start command
@app.on_message(filters.command("start"))
async def start_command_handler(client, message: Message):
    await message.reply("Welcome to the bot! Type /help to see available commands.")

# Define a handler for the /help command
@app.on_message(filters.command("help"))
async def help_command_handler(client, message: Message):
    help_text = """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    """
    await message.reply(help_text)

# Define a handler for messages containing links
@app.on_message(filters.text & filters.regex(r"(http[s]?://\S+)"))
async def link_handler(client, message: Message):
    # Extract the link from the message
    link = re.findall(r"(http[s]?://\S+)", message.text)
    if link:
        # Send a request to the API endpoint
        api_url = f"https://bot-nine-rho.vercel.app/api?data={link[0]}"
        response = requests.get(api_url)
        
        # Check if the request was successful and parse the API response
        if response.status_code == 200:
            api_data = response.json()
            file_name = api_data.get('file_name')
            file_size_str = api_data.get('size')  # Assuming file size is returned as a string
            file_size_bytes = parse_file_size(file_size_str)
            file_link = api_data.get('link')
            direct_link = api_data.get('direct_link')
            thumb_url = api_data.get('thumb')
            
            if all([file_name, file_size_bytes, file_link, direct_link, thumb_url]):
                file_size_mb = file_size_bytes / (1024 * 1024)  # Convert bytes to MB
                size_unit = "MB" if file_size_mb < 1024 else "GB"  # Determine size unit (MB or GB)
                file_size_formatted = f"{file_size_mb:.2f} {size_unit}"
                caption = f"File Name: {file_name}\nFile Size: {file_size_formatted}"
                await message.reply_photo(thumb_url, caption=caption, reply_markup=create_buttons(file_link, direct_link, direct_link))
            else:
                await message.reply("Required data not found in API response.")
        else:
            await message.reply("Error fetching data from the API")

def parse_file_size(file_size_str):
    # Extract numerical part of file size string and convert to bytes
    match = re.match(r'(\d+(\.\d+)?)\s*(KB|MB|GB)', file_size_str)
    if match:
        size_value = float(match.group(1))
        size_unit = match.group(3)
        if size_unit == 'KB':
            return int(size_value * 1024)
        elif size_unit == 'MB':
            return int(size_value * 1024 * 1024)
        elif size_unit == 'GB':
            return int(size_value * 1024 * 1024 * 1024)
    return 0  # Default to 0 bytes if parsing fails

def create_buttons(file_link, direct_link, video_link):
    buttons = [
        [InlineKeyboardButton("Download (Server 1)", url=file_link)],
        [InlineKeyboardButton("Download (Server 2)", url=direct_link)],
        [InlineKeyboardButton("Download Video", url=f"https://t.me/TAD_TeraboxBypaasBot")]
    ]
    return InlineKeyboardMarkup(buttons)


# Start the bot
app.run()
