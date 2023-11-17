import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a rotating file handler
handler = RotatingFileHandler('logs/app.log', maxBytes=100000, backupCount=5)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Initialize bot with token
bot = Bot(token='6589544541:AAFccU96VKGXGiBwY2ycNvDujHCcK7ohYkw')
# Initialize dispatcher
dp = Dispatcher(bot)

# Handler for new chat members
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    try:
        # Get the new member's status in the '@rabota_vmoskve_i_mo' chat
        member_status = await bot.get_chat_member(chat_id='@rabota_vmoskve_i_mo', user_id=message.new_chat_members[0].id)
        # If the new member is not a member of the chat
        if member_status.status == 'left':
            print(member_status)
            # Create a custom keyboard with a "Subscribed to channel" button
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Я Подписался на канал', callback_data='subscribed'))
            # Send a message to the '@msk_24_work' chat
            # await bot.send_message(chat_id='@msk_24_work', text=f'Привет, {message.new_chat_members[0].first_name}! Чтобы иметь возможность писать в чат, необходимо подписаться на канал @rabota_vmoskve_i_mo и ознакомиться с правилами.', reply_markup=keyboard)
            # Restrict the user from sending messages in the '@msk_24_work' chat
            await bot.restrict_chat_member(chat_id='@msk_24_work', user_id=message.new_chat_members[0].id, can_send_messages=False)
            # Log the event
            logging.info(f'User {message.new_chat_members[0].id} joined the chat, but did not subscribe to the channel.')
        else:
            # Log the event
            logging.info(f'User {message.new_chat_members[0].id} joined the chat and subscribed to the channel.')
            # Send a message to the '@msk_24_work' chat
            await bot.send_message(chat_id='@msk_24_work', text=f'Привет, {message.new_chat_members[0].first_name}! Теперь вы можете писать в чат.')
    except Exception as e:
        # Log any errors
        logging.error(f'An error occurred: {e}')


# Handler for callback queries
@dp.callback_query_handler(lambda c: c.data == 'subscribed')
async def process_callback_subscribed(callback_query: types.CallbackQuery):
    try:
        # Get the user's status in the '@rabota_vmoskve_i_mo' chat
        member_status = await bot.get_chat_member(chat_id='@rabota_vmoskve_i_mo', user_id=callback_query.from_user.id)
        print(member_status)
        # If the user is a member of the chat
        if member_status.status != 'left':
            # Give the user the permission to send messages
            await bot.restrict_chat_member(chat_id='@msk_24_work', user_id=callback_query.from_user.id, can_send_messages=True)
            # Send a message to the '@msk_24_work' chat
            await bot.send_message(chat_id='@msk_24_work', text=f'Поздравляю, {callback_query.from_user.first_name}! Теперь вы можете писать в чат.')
            # Log the event
            logging.info(f'User {callback_query.from_user.id} subscribed to the channel and is now allowed to send messages.')
        else:
            # Log the event
            logging.info(f'User {callback_query.from_user.id} clicked the "Subscribed to channel" button, but did not subscribe to the channel.')
            # Send a message to the '@msk_24_work' chat
            await bot.send_message(chat_id='@msk_24_work', text=f'Извините, {callback_query.from_user.first_name}, но вы не подписались на канал.')
    except Exception as e:
        # Log any errors
        logging.error(f'An error occurred: {e}')


# Handler for left chat members
@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def left_member(message: types.Message):
    try:
        # Get the left member's status in the '@rabota_vmoskve_i_mo' chat
        member_status = await bot.get_chat_member(chat_id='@rabota_vmoskve_i_mo', user_id=message.left_chat_member.id)
        # If the left member is not a member of the chat
        if member_status.status == 'left':
            # Log the event
            logging.info(f'User {message.left_chat_member.username} left the chat and did not subscribe to the channel.')
        else:
            # Log the event
            logging.info(f'User {message.left_chat_member.username} left the chat and subscribed to the channel.')
    except Exception as e:
        # Log any errors
        logging.error(f'An error occurred: {e}')


@dp.chat_member_handler()
async def chat_member_handler(chat_member_updated: types.ChatMemberUpdated):
    try:
        print(f'{chat_member_updated.to_python()} Обновления')
        print("Получаем статус нового участника в чате '@rabota_vmoskve_i_mo'")
        # Get the new member's status in the '@rabota_vmoskve_i_mo' chat
        member_status = await bot.get_chat_member(chat_id='@rabota_vmoskve_i_mo', user_id=chat_member_updated.new_chat_member.user.id)
        print(f"Статус нового участника: {member_status.status}")
        # If the new member is not a member of the chat
        if member_status.status == 'left':
            print(f"Пользователь {chat_member_updated.new_chat_member.user.id} присоединился к чату, но не подписался на канал.")
            # Log the event
            logging.info(f'User {chat_member_updated.new_chat_member.user.id} joined the chat, but did not subscribe to the channel.')
            # Create a custom keyboard with a "Subscribed to channel" button
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Я Подписался на канал', callback_data='subscribed'))
            # Send a message to the '@msk_24_work' chat
            await bot.send_message(chat_id='@msk_24_work', text=f'Привет, {chat_member_updated.new_chat_member.user.first_name}! Чтобы иметь возможность писать в чат, необходимо подписаться на канал @rabota_vmoskve_i_mo и ознакомиться с правилами. update', reply_markup=keyboard)
            # Restrict the user from sending messages in the '@msk_24_work' chat
            await bot.restrict_chat_member(chat_id='@msk_24_work', user_id=chat_member_updated.new_chat_member.user.id, can_send_messages=False)
        else:
            print(f"Пользователь {chat_member_updated.new_chat_member.user.id} присоединился к чату и подписался на канал.")
            # Log the event
            logging.info(f'User {chat_member_updated.new_chat_member.user.id} joined the chat and subscribed to the channel.')
            # Send a message to the '@msk_24_work' chat
            # await bot.send_message(chat_id='@msk_24_work', text=f'Привет, {chat_member_updated.new_chat_member.user.first_name}! Теперь вы можете писать в чат.')
    except Exception as e:
        # Log any errors
        print(f"Произошла ошибка: {e}")
        logging.error(f'An error occurred: {e}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, allowed_updates=types.AllowedUpdates.all())
