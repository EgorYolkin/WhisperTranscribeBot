import time

from aiogram import Router, types, F

from src.presentation.app_presentation import AppPresentation
from src.types.models import model_type, Models

handle_audio_router = Router()

PROCESSING_TRANSCRIPT_ANSWER = "Voice is in processing"


@handle_audio_router.message(F.voice | F.audio | F.document)
async def handle_audio(message: types.Message):
    await message.answer(PROCESSING_TRANSCRIPT_ANSWER)

    file_info = await message.bot.get_file(
        message.voice.file_id if message.voice else (
            message.audio.file_id if message.audio else message.document.file_id))
    file_path = file_info.file_path
    downloaded_file = await message.bot.download_file(file_path)

    local_filename = f"data/{message.from_user.id}_{int(time.time())}.ogg"
    with open(local_filename, "wb") as f:
        f.write(downloaded_file.read())

    model: model_type = Models.base

    app_presentation = AppPresentation(
        audio_path=local_filename,
        model_type_raw=model,
        disable_warnings=True,
        duration_showing=True
    )

    await message.answer(app_presentation())
