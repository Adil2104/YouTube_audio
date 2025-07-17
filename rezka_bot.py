import os
import ssl
import certifi
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from yt_dlp import YoutubeDL
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context

API_TOKEN = '8082001963:AAGNa94WvuF23kfJhfE7xEp8BvVbf3ATqeA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.reply("🎵 Пришли мне ссылку на YouTube, и я отправлю тебе аудио.")


@dp.message_handler()
async def handle_message(message: types.Message):
    url = message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await message.reply("❌ Это не ссылка на YouTube.")
        return
    await bot.send_chat_action(message.chat.id, action="upload_audio")
    loading_msg = await message.reply("🌀 Загрузка аудио... Подождите немного...")

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

        # 🔄 Конвертация в mp3 с низким битрейтом (128k)
        subprocess.run([
            "ffmpeg", "-i", raw_audio, "-b:a", "128k", "-y", mp3_audio
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(mp3_audio):
            size_mb = os.path.getsize(mp3_audio) / (1024 * 1024)
            if size_mb > 49:
                await message.reply("❌ Аудиофайл слишком большой для отправки в Telegram (более 50 MB).")
            else:
                audio = InputFile(mp3_audio)
                await bot.send_audio(chat_id=message.chat.id, audio=audio)
                await bot.delete_message(message.chat.id, loading_msg.message_id)

        else:
            await message.reply("⚠️ Файл не найден после конвертации.")

    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")

    finally:
        for f in [raw_audio, mp3_audio]:
            if os.path.exists(f):
                os.remove(f)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
