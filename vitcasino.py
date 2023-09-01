import telebot
import sqlite3
import random
from telebot import types
from dotenv import dotenv_values

config = dotenv_values('.env')

TOKEN = config['TOKEN']

bot = telebot.TeleBot(TOKEN)
db = sqlite3.connect('db', check_same_thread=False)
cursor = db.cursor()

best_users_callbacks = ['balance', 'activity']
slots_callbacks = ['run_slots']
colors = ['black', 'red', 'black', 'red', 'black', 'red', 'green']
dice_callbacks = ['run_dice']
coin_callbacks = ['coin_0', 'coin_1']

top_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
slots_items = ['🍎', '🍉', '🍒', '🍓', '🍋', '🔔', '7️⃣']


def create_db():
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY
                                    UNIQUE
                                    NOT NULL,
            user_id         INTEGER UNIQUE
                                    NOT NULL,
            user_first_name TEXT    NOT NULL,
            user_last_name  TEXT,
            username        STRING,
            balance         INTEGER,
            bet             INTEGER,
            games_played    INTEGER,
            games_won       INTEGER,
            games_lost      INTEGER
        );
        '''
    )

    db.commit()


def add_user(
        user_id,
        user_first_name,
        user_last_name,
        username,
        balance,
        bet,
        games_played,
        games_won,
        games_lost
):
    cursor.execute(
        '''
        INSERT INTO users (
            user_id,
            user_first_name,
            user_last_name,
            username,
            balance,
            bet,
            games_played,
            games_won,
            games_lost
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            user_first_name,
            user_last_name,
            username,
            balance,
            bet,
            games_played,
            games_won,
            games_lost
        )
    )

    db.commit()


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    default_balance = 1000
    default_bet = 0
    games_num = 0
    win_num = 0
    lose_num = 0

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row_width = 2

    buttons = [
        types.KeyboardButton('👤 Аккаунт'),
        types.KeyboardButton('🎰 Слоты'),
        types.KeyboardButton('🎁 Бонус'),
        types.KeyboardButton('🎯 Рулетка'),
        types.KeyboardButton('👑 Лучшие игроки'),
        types.KeyboardButton('🎲 Кости'),
        types.KeyboardButton('⚙ Разработчик'),
        types.KeyboardButton('🟡 Монетка')
    ]

    markup.add(*buttons)

    user = cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))

    if user.fetchone() is None:
        add_user(
            user_id=user_id,
            user_first_name=first_name,
            user_last_name=last_name,
            username=username,
            balance=default_balance,
            bet=default_bet,
            games_played=games_num,
            games_won=win_num,
            games_lost=lose_num
        )

        bot.send_photo(
            message.chat.id,
            photo=open('bg.jpg', 'rb'),
            caption=f'🤚🏻 Привет, <b>{message.from_user.first_name}</b>!\n'
                    f'Добро пожаловать на <b>LuxuryCasino</b>. \n\n'
                    f'🎲 Здесь вы можете поиграть в некоторые классические игры и '
                    f'приумножить свой капитал, играя на <b>виртуальную</b> валюту! \n\n'
                    f'🎁 Для <b>новых</b> пользователей '
                    f'имеется подарок - <b>1000</b> стартовых игровых монет. Удачной игры! \n\n'
                    f'📍 Ваш ID: <code>{user_id}</code> \n'
                    f'💰 Ваш баланс: <code>{default_balance}</code> монет \n',
            parse_mode='HTML',
            reply_markup=markup
        )

    else:
        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

        bot.send_photo(
            message.chat.id,
            photo=open('bg.jpg', 'rb'),
            caption=f'Добро пожаловать, <b>{message.from_user.first_name} 🤚🏻</b>\n\n'
                    f'Рады снова видеть тебя на <b>LuxuryCasino</b>.\n'
                    f'Мы сохранили твой баланс, \nможешь приступить к игре!\n\n'
                    f'📍 Твой уникальный id: <code>{user_id}</code> \n'
                    f'💰 Твой баланс: <code>{balance}</code> монет \n', parse_mode='HTML',
            reply_markup=markup
        )


@bot.message_handler(content_types=['text'])
def menu(message):
    user_id = message.from_user.id
    user_id = cursor.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    games_num = cursor.execute('SELECT games_played FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    games_win = cursor.execute('SELECT games_won FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    games_lose = cursor.execute('SELECT games_lost FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    if message.text == '👤 Аккаунт':
        bot.send_photo(
            message.chat.id,
            photo=open('bg.jpg', 'rb'),
            caption=f'👤 <b>Аккаунт</b> - {message.from_user.first_name}\n\n'
                    f'📍 Твой уникальный id: <code>{user_id}</code> \n'
                    f'💰 Твой баланс: <code>{balance}</code> монет \n\n'
                    f'📊 <b>Статистика</b>\n\n'
                    f'🎲 Всего игр: {games_num}\n'
                    f'🏆 Побед: {games_win}\n'
                    f'☠ Поражений: {games_lose}',
            parse_mode='HTML'
        )

    elif message.text == '⚙ Разработчик':
        markup = types.InlineKeyboardMarkup()

        buttons = [
            types.InlineKeyboardButton(text='GitHub', url='https://github.com/VitalijKo'),
            types.InlineKeyboardButton(text='Telegram', url='https://t.me/VitalijKo')
        ]

        markup.add(*buttons)

        bot.send_message(
            message.chat.id,
            text='⚙ <b>Разработчик</b> \n\n'
                 'Я на GitHub и в Telegram!',
            parse_mode='HTML',
            reply_markup=markup
        )

    elif message.text == '🎁 Бонус':
        if balance < 1000:
            cursor.execute(f'UPDATE users SET balance = (balance + 1000) WHERE user_id = "{user_id}"')

            db.commit()

            bot.send_message(
                message.chat.id,
                text=f'🎁 Вам были зачислены <b>1000</b> монет!',
                parse_mode='HTML'
            )

        else:
            bot.send_message(
                message.chat.id,
                text='🚫 <b>Ошибка</b>\n\n'
                     f'🎁 Бонус в размере 1000 монет '
                     f'можно получить, только если ваш баланс '
                     f'составляет <b>менее</b> 1000 монет.\n\n'
                     f'💰 Ваш баланс: <code>{balance}</code> монет',
                parse_mode='HTML'
            )

    elif message.text == '👑 Лучшие игроки':
        markup = types.InlineKeyboardMarkup()

        buttons = [
            types.InlineKeyboardButton(text='По балансу', callback_data='balance'),
            types.InlineKeyboardButton(text='По активности', callback_data='activity')
        ]

        markup.add(*buttons)

        bot.send_message(
            message.chat.id,
            '👑 <b>Лучшие игроки</b>\n\n',
            parse_mode='HTML',
            reply_markup=markup
        )

    elif message.text == '🎰 Слоты':
        default_bet = 0

        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')

        db.commit()

        msg = bot.send_message(
            message.chat.id,
            text=f'🎰 <b>Слоты</b> \n\n'
                 f'Введите сумму ставки.\n'
                 f'Доступно для игры: <code>{balance}</code> монет',
            parse_mode='HTML'
        )

        bot.register_next_step_handler(msg, set_bet, 'slots')

    elif message.text == '🎯 Рулетка':
        default_bet = 0

        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')

        db.commit()

        msg = bot.send_message(
            message.chat.id,
            text=f'🎯 <b>Рулетка</b> \n\n'
                 f'Введите сумму ставки.\n'
                 f'Доступно для игры: <code>{balance}</code> монет',
            parse_mode='HTML'
        )

        bot.register_next_step_handler(msg, set_bet, 'roulette')

    elif message.text == '🎲 Кости':
        default_bet = 0

        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')

        db.commit()

        msg = bot.send_message(
            message.chat.id,
            text=f'🎲 <b>Кости</b> \n\n'
                 f'Введите сумму ставки.\n'
                 f'Доступно для игры: <code>{balance}</code> монет',
            parse_mode='HTML'
        )

        bot.register_next_step_handler(msg, set_bet, 'dice')

    elif message.text == '🟡 Монетка':
        default_bet = 0

        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')

        db.commit()

        msg = bot.send_message(
            message.chat.id,
            text=f'🟡 <b>Монетка</b> \n\n'
                 f'Введите сумму ставки.\n'
                 f'Доступно для игры: <code>{balance}</code> монет',
            parse_mode='HTML'
        )

        bot.register_next_step_handler(msg, set_bet, 'coin')


def set_bet(message, game):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Назад', callback_data=f'change_bet_{game}')
    markup.add(button)

    try:
        default_bet = 0
        user_id = message.from_user.id

        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

        bet = message.text

        if int(balance) >= int(bet) > 0:
            cursor.execute(f'UPDATE users SET bet = {bet} WHERE user_id = "{user_id}"')

            db.commit()

            balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            start_game(message, game)

        else:
            bot.send_message(
                message.chat.id,
                '🚫 <b>Ошибка</b>\n\n'
                'Сумма ставки не должна превышать ваш баланс, а также\n'
                'быть меньше или равной нулю!\n'
                'Попробуйте снова. ',
                parse_mode='HTML',
                reply_markup=markup
            )

            cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')

            db.commit()
    except ValueError:
        default_bet = 0
        user_id = message.from_user.id

        bot.send_message(
            message.chat.id,
            '🚫 <b>Ошибка</b>\n\n'
            'Ставка должна быть числом!\n'
            'Попробуйте снова. ',
            parse_mode='HTML', reply_markup=markup
        )

        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')

        db.commit()


def start_game(message, game):
    user_id = message.from_user.id
    user_bet = cursor.execute('SELECT bet FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    markup = types.InlineKeyboardMarkup()

    if game == 'slots':
        title = '🎰 <b>Слоты</b>'

        buttons = [
            types.InlineKeyboardButton(text='🕹 Крутить', callback_data='run_slots'),
            types.InlineKeyboardButton(text='Изменить ставку', callback_data='change_bet_slots')
        ]

    elif game == 'roulette':
        title = '🎯 <b>Выберите цвет</b>'

        buttons = [
            types.InlineKeyboardButton(text='⚫ Черный', callback_data='black'),
            types.InlineKeyboardButton(text='🔴 Красный', callback_data='red'),
            types.InlineKeyboardButton(text='🟢 Зеленый', callback_data='green'),
            types.InlineKeyboardButton(text='Изменить ставку', callback_data='change_bet_roulette')
        ]

    elif game == 'dice':
        title = '🎲 <b>Кости</b>'

        buttons = [
            types.InlineKeyboardButton(text='🥏 Бросить', callback_data='run_dice'),
            types.InlineKeyboardButton(text='Изменить ставку', callback_data='change_bet_dice')
        ]

    elif game == 'coin':
        title = '🟡 <b>Орел или решка?</b>'

        buttons = [
            types.InlineKeyboardButton(text='🦅 Орел', callback_data='coin_0'),
            types.InlineKeyboardButton(text='🥇 Решка', callback_data='coin_1'),
            types.InlineKeyboardButton(text='Изменить ставку', callback_data='change_bet_coin')
        ]

    markup.add(*buttons)

    bot.send_message(
        message.chat.id,
        f'{title}\n\n'
        f'Баланс: <code>{balance}</code> монет.\n'
        f'Сумма ставки: <code>{user_bet}</code> монет. ',
        parse_mode='HTML',
        reply_markup=markup
    )


def get_best_players(call):
    user_id = call.from_user.id

    if call.data == 'balance':
        cursor.execute(
            '''
            SELECT username, balance, games_played
            FROM users
            ORDER BY balance desc
            LIMIT 10;
            '''
        )

        richest_players = cursor.fetchall()

        output = '💰 <b>Самые богатые игроки</b>\n\n'

        for i, richest_player in enumerate(richest_players):
            output += f'<b>{top_numbers[i]} 👤 {richest_player[0]}</b>\n' \
                      f'💰 Баланс: {richest_player[1]}\n' \
                      f'🎲 Всего игр: {richest_player[2]}\n\n'

        bot.send_photo(
            user_id,
            photo=open('bg.jpg', 'rb'),
            caption=output,
            parse_mode='HTML'
        )

    else:
        cursor.execute(
            '''
            SELECT username, balance, games_played
            FROM users
            ORDER BY games_played desc
            LIMIT 10;
            '''
        )

        most_active_players = cursor.fetchall()

        output = '🎲 <b>Самые активные игроки</b>\n\n'

        for i, most_active_player in enumerate(most_active_players):
            output += f'<b>{top_numbers[i]} 👤 {most_active_player[0]}</b>\n' \
                      f'💰 Баланс: {most_active_player[1]}\n' \
                      f'🎲 Всего игр: {most_active_player[2]}\n\n'

        bot.send_photo(
            user_id,
            photo=open('bg.jpg', 'rb'),
            caption=output,
            parse_mode='HTML'
        )


def slots(call):
    user_id = call.from_user.id

    balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    user_bet = cursor.execute('SELECT bet FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    result = [
        random.choices(slots_items, k=3),
        random.choices(slots_items, k=3),
        random.choices(slots_items, k=3)
    ]

    markup = types.InlineKeyboardMarkup()

    buttons = [
        types.InlineKeyboardButton(text='🕹 Крутить', callback_data='run_slots'),
        types.InlineKeyboardButton(text='Изменить ставку', callback_data='change_bet_slots')
    ]

    markup.add(*buttons)

    if balance < user_bet:
        bot.send_message(
            user_id,
            '🚫 <b>Ошибка</b>\n\n'
            'Сумма ставки не должна превышать ваш баланс, а так же\n'
            'быть меньше или равной нулю!\n'
            'Попробуйте снова. ',
            parse_mode='HTML',
            reply_markup=markup
        )

    else:
        output = ''

        for row in result:
            output += '    '.join(row) + '\n'

        cashout = 0

        result = list(zip(*result))

        for i, reel in enumerate(result):
            result[i] = list(reel)

        for item in result[0]:
            if item in result[1] and item in result[2] and item != '0':
                if item in slots_items[:2]:
                    cashout += 0.5

                if item in slots_items[:4]:
                    cashout += 1

                if item in slots_items[:6]:
                    cashout += 2

                if item == slots_items[6]:
                    cashout += 5

                indexes = [
                    result[0].index(item),
                    result[1].index(item),
                    result[2].index(item)
                ]

                for i, index in enumerate(indexes):
                    result[i][index] = '0'

        if cashout == 15:
            cashout = 100

        output += f'\n\nВы получили: <code>{user_bet * cashout}</code> монет.'

        bot.send_message(
            call.message.chat.id,
            f'<b>{output}</b>',
            parse_mode='HTML'
        )

        if cashout >= 1:
            bot.answer_callback_query(call.id, f'{"Победа!" if cashout < 100 else "Джекпот!"}!')

            cursor.execute(f'UPDATE users SET balance = (balance + bet * {cashout - 1}) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_won = (games_won + 1) WHERE user_id = "{user_id}"')

            db.commit()

            balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            bot.send_message(
                call.message.chat.id,
                f'🎰 <b>{"Победа!" if cashout < 100 else "Джекпот!"}</b>\n\n'
                f'Баланс: <code>{balance}</code> монет.\n'
                f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
                f'Играем дальше?',
                parse_mode='HTML',
                reply_markup=markup
            )

        else:
            bot.answer_callback_query(call.id, 'Вы проиграли!')

            cursor.execute(f'UPDATE users SET balance = (balance + bet * {cashout - 1}) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_lost = (games_lost + 1) WHERE user_id = "{user_id}"')

            db.commit()

            balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            bot.send_message(
                call.message.chat.id,
                f'🎰 <b>Проигрыш!</b>\n\n'
                f'Баланс: <code>{balance}</code> монет.\n'
                f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
                f'Играем дальше?',
                parse_mode='HTML',
                reply_markup=markup
            )


def roulette(call):
    user_id = call.from_user.id

    balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    user_bet = cursor.execute('SELECT bet FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    random_color = str(random.choice(colors))

    markup = types.InlineKeyboardMarkup()

    buttons = [
        types.InlineKeyboardButton(text='⚫ Черный', callback_data='black'),
        types.InlineKeyboardButton(text='🔴 Красный', callback_data='red'),
        types.InlineKeyboardButton(text='🟢 Зеленый', callback_data='green'),
        types.InlineKeyboardButton(text='Изменить ставку', callback_data='change_bet_roulette')
    ]

    markup.add(*buttons)

    if balance < user_bet:
        bot.send_message(
            user_id,
            '🚫 <b>Ошибка</b>\n\n'
            'Сумма ставки не должна превышать ваш баланс, а так же\n'
            'быть меньше или равной нулю!\n'
            'Попробуйте снова. ',
            parse_mode='HTML',
            reply_markup=markup
        )

    elif call.data == 'black' and call.data == random_color:
        bot.answer_callback_query(call.id, 'Победа!')

        cursor.execute(f'UPDATE users SET balance = (balance + bet * 2) WHERE user_id = "{user_id}"')

        db.commit()

        cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

        db.commit()

        cursor.execute(f'UPDATE users SET games_won = (games_won + 1) WHERE user_id = "{user_id}"')

        db.commit()

        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

        bot.send_message(
            call.message.chat.id,
            f'🎯 <b>Победа!</b>\n\n'
            f'Баланс: <code>{balance}</code> монет.\n'
            f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
            f'Играем дальше? Выбери цвет.',
            parse_mode='HTML',
            reply_markup=markup
        )

    elif call.data == 'red' and call.data == random_color:
        bot.answer_callback_query(call.id, 'Победа!')

        cursor.execute(f'UPDATE users SET balance = (balance + bet * 2) WHERE user_id = "{user_id}"')

        db.commit()

        cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

        db.commit()

        cursor.execute(f'UPDATE users SET games_won = (games_won + 1) WHERE user_id = "{user_id}"')

        db.commit()

        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

        bot.send_message(
            call.message.chat.id,
            f'🎯 <b>Победа!</b>\n\n'
            f'Баланс: <code>{balance}</code> монет.\n'
            f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
            f'Играем дальше? Выбери цвет.',
            parse_mode='HTML',
            reply_markup=markup
        )

    elif call.data == 'green' and call.data == random_color:
        bot.answer_callback_query(call.id, 'Победа!')

        cursor.execute(f'UPDATE users SET balance = (balance + bet * 7) WHERE user_id = "{user_id}"')

        db.commit()

        cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

        db.commit()

        cursor.execute(f'UPDATE users SET games_won = (games_won + 1) WHERE user_id = "{user_id}"')

        db.commit()

        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

        bot.send_message(
            call.message.chat.id,
            f'🎯 <b>Победа!</b>\n\n'
            f'Баланс: <code>{balance}</code> монет.\n'
            f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
            f'Играем дальше? Выбери цвет.',
            parse_mode='HTML',
            reply_markup=markup
        )

    else:
        bot.answer_callback_query(call.id, 'Вы проиграли!')

        cursor.execute(f'UPDATE users SET balance = (balance - bet) WHERE user_id = "{user_id}"')

        db.commit()

        cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

        db.commit()

        cursor.execute(f'UPDATE users SET games_lost = (games_lost + 1) WHERE user_id = "{user_id}"')

        db.commit()

        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

        bot.send_message(
            call.message.chat.id,
            f'🎯 <b>Проигрыш!</b>\n\n'
            f'Баланс: <code>{balance}</code> монет.\n'
            f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
            f'Играем дальше? Выбери цвет.',
            parse_mode='HTML',
            reply_markup=markup
        )


def dice(call):
    user_id = call.from_user.id

    balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    user_bet = cursor.execute('SELECT bet FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    casino_number = random.randint(1, 12)
    user_number = random.randint(1, 12)

    markup = types.InlineKeyboardMarkup()

    buttons = [
        types.InlineKeyboardButton(text='🥏 Бросить', callback_data='run_dice'),
        types.InlineKeyboardButton(text='Изменить ставку', callback_data='change_bet_dice')
    ]

    markup.add(*buttons)

    if balance < user_bet:
        bot.send_message(
            user_id,
            '🚫 <b>Ошибка</b>\n\n'
            'Сумма ставки не должна превышать ваш баланс, а так же\n'
            'быть меньше или равной нулю!\n'
            'Попробуйте снова. ',
            parse_mode='HTML',
            reply_markup=markup
        )

    else:
        bot.send_message(
            call.message.chat.id,
            f'<b>Число казино:</b> <code>{casino_number}</code>.\n'
            f'<b>Ваше число:</> <code>{user_number}</code>.\n\n',
            parse_mode='HTML'
        )

        if user_number >= casino_number:
            bot.answer_callback_query(call.id, 'Победа!')

            cursor.execute(f'UPDATE users SET balance = (balance + bet * 2) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_won = (games_won + 1) WHERE user_id = "{user_id}"')

            db.commit()

            balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            bot.send_message(
                call.message.chat.id,
                f'🎲 <b>Победа!</b>\n\n'
                f'Баланс: <code>{balance}</code> монет.\n'
                f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
                f'Играем дальше?',
                parse_mode='HTML',
                reply_markup=markup
            )

        elif user_number < casino_number:
            bot.answer_callback_query(call.id, 'Вы проиграли!')

            cursor.execute(f'UPDATE users SET balance = (balance - bet) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_lost = (games_lost + 1) WHERE user_id = "{user_id}"')

            db.commit()

            balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            bot.send_message(
                call.message.chat.id,
                f'🎲 <b>Проигрыш!</b>\n\n'
                f'Баланс: <code>{balance}</code> монет.\n'
                f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
                f'Играем дальше?',
                parse_mode='HTML',
                reply_markup=markup
            )


def coin(call):
    user_id = call.from_user.id

    balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    user_bet = cursor.execute('SELECT bet FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    result = random.randint(0, 1)
    choice = int(call.data.split('coin_')[1])

    markup = types.InlineKeyboardMarkup()

    buttons = [
        types.InlineKeyboardButton(text='🦅 Орел', callback_data='coin_0'),
        types.InlineKeyboardButton(text='🥇 Решка', callback_data='coin_1'),
        types.InlineKeyboardButton(text='Изменить ставку', callback_data='change_bet_coin')
    ]

    markup.add(*buttons)

    if balance < user_bet:
        bot.send_message(
            user_id,
            '🚫 <b>Ошибка</b>\n\n'
            'Сумма ставки не должна превышать ваш баланс, а так же\n'
            'быть меньше или равной нулю!\n'
            'Попробуйте снова. ',
            parse_mode='HTML',
            reply_markup=markup
        )

    else:
        bot.send_message(
            call.message.chat.id,
            f'<b>Выпало:</b> <code>{"🥇 Решка" if result else "🦅 Орел"}</code>.\n',
            parse_mode='HTML'
        )

        if choice is result:
            bot.answer_callback_query(call.id, 'Победа!')

            cursor.execute(f'UPDATE users SET balance = (balance + bet * 2) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_won = (games_won + 1) WHERE user_id = "{user_id}"')

            db.commit()

            balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            bot.send_message(
                call.message.chat.id,
                f'🟡 <b>Победа!</b>\n\n'
                f'Баланс: <code>{balance}</code> монет.\n'
                f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
                f'Играем дальше?',
                parse_mode='HTML',
                reply_markup=markup
            )

        else:
            bot.answer_callback_query(call.id, 'Вы проиграли!')

            cursor.execute(f'UPDATE users SET balance = (balance - bet) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_played = (games_played + 1) WHERE user_id = "{user_id}"')

            db.commit()

            cursor.execute(f'UPDATE users SET games_lost = (games_lost + 1) WHERE user_id = "{user_id}"')

            db.commit()


            balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            bot.send_message(
                call.message.chat.id,
                f'🟡 <b>Проигрыш!</b>\n\n'
                f'Баланс: <code>{balance}</code> монет.\n'
                f'Сумма ставки: <code>{user_bet}</code> монет.\n\n'
                f'Играем дальше?',
                parse_mode='HTML',
                reply_markup=markup
            )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id

    if call.data in best_users_callbacks:
        get_best_players(call)

    elif call.data in slots_callbacks:
        slots(call)

    elif call.data in colors:
        roulette(call)

    elif call.data in dice_callbacks:
        dice(call)

    elif call.data in coin_callbacks:
        coin(call)

    elif call.data.startswith('change_bet_'):
        game = call.data.split('change_bet_')[1]

        if game == 'slots':
            title = '🎰 <b>Слоты</b>'

        elif game == 'roulette':
            title = '🎯 <b>Рулетка</b>'

        elif game == 'dice':
            title = '🎲 <b>Кости</b>'

        elif game == 'coin':
            title = '🟡 <b>Монетка</b>'

        default_bet = 0

        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')

        db.commit()

        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

        msg2 = bot.send_message(
            user_id,
            text=f'{title} \n\n'
                 f'Введите сумму ставки.\n'
                 f'Доступно для игры: <code>{balance}</code> монет',
            parse_mode='HTML'
        )

        bot.register_next_step_handler(msg2, change_bet, game)


def change_bet(message, game):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Назад', callback_data=f'change_bet_{game}')
    markup.add(button)

    try:
        default_bet = 0

        user_id = message.from_user.id

        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

        bet = message.text

        if int(balance) >= int(bet) > 0:
            cursor.execute(f'UPDATE users SET bet = "{bet}" WHERE user_id = "{user_id}"')

            db.commit()

            balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            start_game(message, game)

        else:
            bot.send_message(
                message.chat.id,
                '🚫 <b>Ошибка</b>\n\n'
                'Сумма ставки не должна превышать ваш баланс, а так же\n'
                'быть меньше или равной нулю!\n'
                'Попробуйте снова. ',
                parse_mode='HTML',
                reply_markup=markup
            )

            cursor.execute(f'UPDATE users SET bet = {default_bet} WHERE user_id = "{user_id}"')

            db.commit()
    except:
        default_bet = 0

        user_id = message.from_user.id

        bot.send_message(
            message.chat.id,
            '🚫 <b>Ошибка</b>\n\n'
            'Ставка должна быть числом!\n'
            'Попробуйте снова. ',
            parse_mode='HTML',
            reply_markup=markup
        )

        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')

        db.commit()


create_db()
bot.infinity_polling()
