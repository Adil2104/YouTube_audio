
import os
import ssl
import certifi
import asyncio
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatAction
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from yt_dlp import YoutubeDL

ssl._create_default_https_context = ssl._create_unverified_context

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("🎵 Пришли мне ссылку на YouTube, и я отправлю тебе аудио.⚠️ Максимальная длина видео — 10 минут.")

@dp.message()
async def handle_message(message: Message):
    url = message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await message.reply("❌ Это не ссылка на YouTube.")
        return

    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    loading_msg = await message.reply("⏳ Загрузка аудио... Пожалуйста, подождите.")

    raw_audio = "audio.webm"
    mp3_audio = "audio.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': raw_audio,
        'noplaylist': True,
        'quiet': True,
        'merge_output_format': 'webm',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # 🔁 Конвертация в mp3
        subprocess.run(['ffmpeg', '-y', '-i', raw_audio, '-b:a', '192k', mp3_audio], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 📤 Отправка mp3
        await bot.send_audio(chat_id=message.chat.id, audio=types.FSInputFile(mp3_audio))

    except Exception as e:
        await message.reply(f"❌ Произошла ошибка при загрузке: {e}")

    finally:
        await loading_msg.delete()
        for f in (raw_audio, mp3_audio):
            if os.path.exists(f):
                os.remove(f)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
