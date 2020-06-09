from core.resources import strings, keyboards
from telegram.ext import BaseFilter
from core.services import users


class Navigation:
    @staticmethod
    def to_main_menu(update, language, message_text=None, user_name=None):
        if message_text:
            menu_message = message_text
        else:
            menu_message = strings.get_string('start.welcome', language).format(username=user_name)
        menu_keyboard = keyboards.get_keyboard('menu', language)
        update.message.reply_text(menu_message, reply_markup=menu_keyboard)

    @staticmethod
    def to_account(update, context):
        if 'user' not in context.user_data:
            if update.message:
                user_id = update.message.from_user.id
            elif update.callback_query:
                user_id = update.callback_query.from_user.id
            context.user_data['user'] = users.user_exists(user_id)
        user = context.user_data['user']
        account_message = strings.get_user_info(user)
        account_keyboard = keyboards.get_account_keyboard(user)
        if update.message:
            update.message.reply_text(text=account_message, reply_markup=account_keyboard)
        elif update.callback_query:
            context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=account_message, reply_markup=account_keyboard)


class Filters:
    class AccountFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.cabinet', 'ru') in message.text or
                                     strings.get_string('menu.cabinet', 'uz') in message.text)
