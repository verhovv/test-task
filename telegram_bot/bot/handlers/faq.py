from aiogram import Router, F
from aiogram.types import InlineQuery, Message, InlineQueryResultArticle, InputTextMessageContent

from main_app.models import FAQ, User
from .. import keyboards
from ..texts import get_menu_text

router = Router()


@router.inline_query()
async def faq_inline(inline_query: InlineQuery):
    questions = list()

    async for faq in FAQ.objects.all():
        questions.append(faq.question)

    questions.sort(
        key=lambda x: (
            not inline_query.query.lower() in x.lower(),
            -sum(letter in x.lower() for letter in set(inline_query.query.lower()))
        )
    )

    if questions:
        results = list()
        for i, question in enumerate(questions):
            results.append(InlineQueryResultArticle(
                title=question, id=str(i),
                input_message_content=InputTextMessageContent(message_text=question),
            ))

        await inline_query.answer(
            results, cache_time=0
        )

@router.message(F.text.in_([x.question for x in FAQ.objects.all()]))
async def on_message(message: Message, user: User):
    answer = await FAQ.objects.aget(question=message.text)
    await message.answer(text=answer.answer)
    await message.answer(text=get_menu_text(user=user), reply_markup=keyboards.get_menu_keyboard())
