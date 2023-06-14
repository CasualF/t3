import csv
import telebot
from decouple import config
from telebot import types
import markups


TOKEN = config("TOKEN")
bot = telebot.TeleBot(TOKEN)


class Task:
    def __init__(self, name, des, date, status=False):
        self.name = name
        self.des = des
        self.date = date
        self.status = status

    def mark_as_done(self) -> None:
        self.status = True

    def mark_as_undonde(self) -> None:
        self.status = False

    def edit_description(self, des):
        self.des = des

    def __str__(self):
        return (
            f'{self.name} - {self.des}\n{self.date}\nCurrently isdone -> {self.status}'
        )


class TaskList:
    ls = []
    str_ls = []

    def create_task(self, name, des, date, status=False):
        # for i in self.ls:
        #     if name == i['name']:
        #         return 'Already exists'
        # self.ls.append(
        #     {'name': name, 'description': des, 'date': date, 'status': status}
        # )
        # return '
        task = {'name': name, 'description': des, 'date': date, 'status': status}
        string = Task(name, des, date, status)
        self.ls.append(task)
        self.str_ls.append(str(string))

    def get_task(self, search):
        for i in self.ls:
            if search == i['name']:
                return self.str_ls[self.ls.index(i)]
        return 'Not Found'

    def remove_task(self, name):
        for i in self.ls:
            if i['name'] == name:
                self.ls.remove(i)
                return 'Deleted'
        return 'Not Found'

    def get_all_tasks(self):
        return self.ls

    def __len__(self):
        return len(self.ls)

    def get_string_tasks(self):
        return self.str_ls


def log_activity(func):
    def wrapper():
        func()

    return wrapper


obj = TaskList()


@bot.message_handler(commands=['start'])
def start_s(message):
    global msg
    msg = message
    obj = TaskList()
    bot.send_message(
        message.chat.id,
        "Hello, This bot can keep you up with your tasks!",
        reply_markup=markups.options
    )


@bot.message_handler(func=lambda x: x.text == 'Check all tasks')
def check_tasks(message):
    bot.send_message(message.chat.id, 'ToDo:', reply_markup=markups.crud)
    if obj.str_ls:
        for i in range(len(obj.str_ls)):
            bot.send_message(message.chat.id, f'{i+1}.{obj.str_ls[i]}')
    else:
        bot.send_message(
            message.chat.id,
            'Currently there are no tasks in your ToDo list, make one!',
            reply_markup=markups.crud,
        )
@bot.message_handler(func=lambda x: x.text == 'Create task')
def creating_name(message):
    global name, des, date, n1, des1, date1
    name = '**Name of your task**'
    des = '**Some description**'
    date = '**Date related information**'

    n1 = False
    des1 = False
    date1 = False


    bot.send_message(message.chat.id, f'{name}\n{des}\n{date}')
    bot.send_message(
        message.chat.id, 'Choose to make change ', reply_markup=markups.create
    )

    @bot.message_handler(func=lambda x: x.text == 'Put Name')
    def naming(message):
        global n1
        bot.send_message(message.chat.id, 'Whats the name of your task?')
        n1 = True
        bot.register_next_step_handler(message, getting_name)

    @bot.message_handler(func=lambda msg:True and n1)
    def getting_name(message):
        global name, n1
        name = message.text
        bot.send_message(message.chat.id, f'{name}\n{des}\n{date}')
        n1 = False

    @bot.message_handler(func=lambda x: x.text == 'Put Description')
    def desing(message):
        global des1
        bot.send_message(message.chat.id, 'Add some description:')
        des1 = True
        bot.register_next_step_handler(message, getting_des)
    @bot.message_handler(func=lambda msg:True and des1)
    def getting_des(message):
        global des , des1
        des = message.text
        bot.send_message(message.chat.id, f'{name}\n{des}\n{date}')
        des1 = False

    @bot.message_handler(func=lambda x: x.text == 'Put Date')
    def dating(message):
        global date1
        bot.send_message(message.chat.id, 'Type date/deadline related info:')
        date1 = True
        bot.register_next_step_handler(message, getting_date)
    @bot.message_handler(func=lambda msg:True and date1)
    def getting_date(message):
        global date, date1
        date = message.text
        bot.send_message(message.chat.id, f'{name}\n{des}\n{date}')
        date1 = False

    @bot.message_handler(func=lambda x: x.text == 'Finish')
    def finishing(message):
        bot.send_message(message.chat.id, f'{name}\n{des}\n{date}')


@bot.message_handler(func=lambda x: x.text == 'Quit')
def quitting(message):
    bot.send_message(
        message.chat.id,
        "Farewell\nTo start me up --> /start",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'checking':
        check_tasks(msg)
    elif call.data == 'quitting':
        quitting(msg)


bot.polling()
