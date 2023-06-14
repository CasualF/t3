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
            f'{self.name}\n{self.des}\n{self.date}\nCurrently isdone -> {self.status}'
        )


class TaskList:
    ls = []

    def create_task(self, name, des, date, status=False):
        task = {'name': name, 'description': des, 'date': date, 'status': status}
        self.ls.append(task)

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


def log_activity(func):
    def wrapper():
        func()

    return wrapper


read_mode = False
update_mode = False
delete_mode = False


@bot.message_handler(commands=['start'])
def start_s(message):
    global msg, obj
    msg = message
    obj = TaskList()
    bot.send_message(
        message.chat.id,
        "Hello, This bot can keep you up with your tasks!",
        reply_markup=markups.options,
    )


@bot.message_handler(func=lambda x: x.text == 'Check all tasks')
def check_tasks(message):
    bot.send_message(message.chat.id, 'ToDo:', reply_markup=markups.crud)
    if obj.ls:
        for i in range(obj.__len__()):
            if obj.ls[i]['status']:
                sen = f'{i+1}.{obj.ls[i]["name"]} ✅'
            else:
                sen = f'{i+1}.{obj.ls[i]["name"]}'
            bot.send_message(message.chat.id, sen)
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

    @bot.message_handler(func=lambda msg: True and n1)
    def getting_name(message):
        global name, n1
        name = message.text
        bot.send_message(message.chat.id, f'{name}\n{des}\n{date}')
        n1 = False

    @bot.message_handler(func=lambda x: x.text == 'Put Description')
    def desing(message):
        global des1
        bot.send_message(message.chat.id, 'Whats the description:')
        des1 = True
        bot.register_next_step_handler(message, getting_des)

    @bot.message_handler(func=lambda msg: True and des1)
    def getting_des(message):
        global des, des1
        des = message.text
        bot.send_message(message.chat.id, f'{name}\n{des}\n{date}')
        des1 = False

    @bot.message_handler(func=lambda x: x.text == 'Put Date')
    def dating(message):
        global date1
        bot.send_message(message.chat.id, 'Type date/deadline related info:')
        date1 = True
        bot.register_next_step_handler(message, getting_date)

    @bot.message_handler(func=lambda msg: True and date1)
    def getting_date(message):
        global date, date1
        date = message.text
        bot.send_message(message.chat.id, f'{name}\n{des}\n{date}')
        date1 = False

    @bot.message_handler(func=lambda x: x.text == 'Finish')
    def finishing(message):
        for i in obj.ls:
            if name == i['name']:
                bot.send_message(message.chat.id, 'Task with that name already exists')
        obj.create_task(name, des, date)
        bot.send_message(
            message.chat.id, 'Done! Task created', reply_markup=markups.options
        )


@bot.message_handler(func=lambda x: x.text == 'Read task')
def reading(message):
    global read_mode
    read_mode = True
    bot.send_message(
        message.chat.id,
        'Choose the task you\'re interested in by number:',
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(
    func=lambda x: x.text.isdigit()
    and int(x.text) in range(1, len(obj.ls) + 1)
    and read_mode
)
def retrieve(message):
    read_id = int(message.text) - 1
    global read_mode
    read_mode = False
    bot.send_message(
        message.chat.id,
        f'{obj.ls[read_id]["name"]}\n{obj.ls[read_id]["description"]}\n{obj.ls[read_id]["date"]}\nCurrently isdone -> {obj.ls[read_id]["status"]}',
        reply_markup=markups.options,
    )


@bot.message_handler(func=lambda x: x.text == 'Update task')
def upping(message):
    global update_mode
    update_mode = True
    bot.send_message(
        message.chat.id,
        'Choose the task you\'re interested in by number:',
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(
    func=lambda x: x.text.isdigit()
    and int(x.text) in range(1, len(obj.ls) + 1)
    and update_mode
)
def updating(message):
    global selected_id, update_mode
    selected_id = int(message.text)
    update_mode = False
    name = obj.ls[int(message.text) - 1]['name']
    des = obj.ls[int(message.text) - 1]['description']
    date = obj.ls[int(message.text) - 1]['date']
    bot.send_message(
        message.chat.id,
        'What you wanna do with this task?',
        reply_markup=markups.update,
    )


@bot.message_handler(func=lambda x: x.text == 'Quit')
def quitting(message):
    bot.send_message(
        message.chat.id,
        "Farewell\nTo start me up --> /start",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(func=lambda x: x.text == 'I\'m good')
def goochi(message):
    bot.send_message(message.chat.id, 'Okay', reply_markup=markups.options)


@bot.message_handler(func=lambda x: x.text == 'Status -> Done')
def status_on(message):
    obj.ls[selected_id - 1]['status'] = True
    bot.send_message(
        message.chat.id, 'Status changed to True', reply_markup=markups.options
    )


@bot.message_handler(func=lambda x: x.text == 'Status -> Undone')
def status_on(message):
    obj.ls[selected_id - 1]['status'] = False
    bot.send_message(
        message.chat.id, 'Status changed to False', reply_markup=markups.options
    )


@bot.message_handler(func=lambda x:x.text == 'Delete task')
def deleting(message):
    global delete_mode
    delete_mode = True
    bot.send_message(
        message.chat.id,
        'Choose the task you\'re interested in by number:',
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(
    func=lambda x: x.text.isdigit()
    and int(x.text) in range(1, len(obj.ls) + 1)
    and delete_mode
)
def delling(message):
    delete_id = int(message.text) - 1
    obj.ls.remove(obj.ls[delete_id])
    bot.send_message(message.chat.id, 'Task deleted', reply_markup=markups.options)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'checking':
        check_tasks(msg)
    elif call.data == 'quitting':
        quitting(msg)


bot.polling()
