import telebot
from telebot import types


crud = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
bt1 = types.KeyboardButton('Create task')
bt2 = types.KeyboardButton('Read task')
bt3 = types.KeyboardButton('Update task')
bt4 = types.KeyboardButton('Delete task')
bt5 = types.KeyboardButton('Quit')
crud.add(bt1,bt2,bt3,bt4)
crud.add(bt5)

options = types.ReplyKeyboardMarkup(row_width=1)
op1 = types.KeyboardButton('Check all tasks')
op2 = types.KeyboardButton('Quit')
options.add(op1, op2)

create = types.ReplyKeyboardMarkup(row_width=3)
cr1 = types.KeyboardButton('Put Name')
cr2 = types.KeyboardButton('Put Description')
cr3 = types.KeyboardButton('Put Date')
cr4 = types.KeyboardButton('Finish')
create.add(cr1,cr2,cr3,cr4)


update = types.ReplyKeyboardMarkup(row_width=3)
on = types.KeyboardButton('Status -> Done')
off = types.KeyboardButton('Status -> Undone')
last = types.KeyboardButton('I\'m good')
update.add(cr1,cr2,cr3,on,off)
update.add(last)

