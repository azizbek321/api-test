import sys
import os

# ✅ Asosiy loyiha papkasini Python path ga qo'shish
# bot/ papkasidan bir yuqoriga chiqamiz (amalyot copy/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ✅ Django settings ni ko'rsatamiz
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  
# yoki "amalyot copy.settings" — settings.py qayerda bo'lsa

# ✅ Django ni ishga tushiramiz (modellardan OLDIN!)
import django
django.setup()
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import logging
import asyncio
from products.models import Product

bot = Bot(token="8059780984:AAE62wTsNMUIrbwZKWu8xbPzq9RQzkizUew")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@sync_to_async
def get_all_products():
    return list(Product.objects.all())


@dp.message(CommandStart())
async def StarBot(message: Message):
    await message.answer(f"Hi {message.from_user.full_name}, {get_all_products()}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("tugadi")