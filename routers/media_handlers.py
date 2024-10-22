from aiogram import Router, F, types

router = Router()


@router.message(F.photo, ~F.caption)
async def handle_photo_wo_caption(message: types.Message):
    caption = "Can't see, sorry"
    await message.reply_photo(
        photo=message.photo[-1].file_id,
        caption=caption
    )


@router.message(F.photo, F.caption.contains("please"))
async def handle_photo_with_please_caption(message: types.Message):
    await message.reply("Can't see")


any_media_filter = F.photo | F.video | F.document


@router.message(any_media_filter, ~F.caption)
async def handle_any_media_wo_caption(message: types.Message):
    if message.document:
        await message.reply_document(
            document=message.document.file_id,
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id
        )
    else:
        await message.reply("I can't see any media")
