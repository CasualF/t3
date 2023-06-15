import datetime
import curses
import json

class Task:
    def __init__(self, title, description, status='не выполнено'):
        self.title = title
        self.description = description
        self.status = status
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def mark_as_done(self):
        self.status = 'выполнено'

    def mark_as_undone(self):
        self.status = 'не выполнено'

    def edit_description(self, new_description):
        self.description = new_description

    def __str__(self):
        return f"Название: {self.title}\nОписание: {self.description}\nСтатус: {self.status}\nДата создания: {self.creation_date}\n"


class TaskList:
    def __init__(self):
        self.tasks = []

    def create_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_to_json()

    def get_task(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        elif index == -1:
            return -1
        else:
            return None

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_json()
        elif index == -1:
            self.tasks = []
            self.save_to_json()

    def get_all_tasks(self):
        return self.tasks

    def save_to_json(self):
        tasks_data = []
        for task in self.tasks:
            task_data = {
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'creation_date': task.creation_date
            }
            tasks_data.append(task_data)

        with open('tasks.json', 'w') as file:
            json.dump(tasks_data, file)

    def load_from_json(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task(task_data['title'], task_data['description'], task_data['status'])
                    task.creation_date = task_data['creation_date']
                    self.tasks.append(task)
        except FileNotFoundError:
            pass


def initialize_screen():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()
    return stdscr

def get_numeric_input(stdscr):
    while True:
        user_input = stdscr.getstr().decode()
        if user_input.isdigit():
            return int(user_input)
        else:
            stdscr.addstr("Пожалуйста, введите только цифру.\n")


def print_tasks(stdscr, task_list):
    stdscr.clear()
    stdscr.addstr("Список задач:\n\n")
    tasks = task_list.get_all_tasks()
    for index, task in enumerate(tasks):
        stdscr.addstr(f"{index + 1}. {task.title} ({task.status})\n")
    stdscr.refresh()
    
def info_tasks(stdscr, task_list):
    stdscr.clear()
    stdscr.addstr("Список задач:\n\n")
    tasks = task_list.get_all_tasks()
    for task in tasks:
        stdscr.addstr(task.__str__())
        stdscr.addstr('\n')
    stdscr.addstr("\nНажмите любую клавишу для продолжения.")
    stdscr.refresh()
    stdscr.getch()

def create_task(stdscr, task_list):
    stdscr.clear()
    stdscr.addstr("Создание новой задачи\n\n")
    stdscr.addstr("Введите название задачи: ")
    stdscr.refresh()
    curses.echo()
    title = stdscr.getstr().decode()
    stdscr.addstr("Введите описание задачи: ")
    description = stdscr.getstr().decode()  # Получить полный ввод до нажатия Enter
    curses.noecho() 
    task_list.create_task(title, description)
    stdscr.addstr("Задача успешно создана. Нажмите любую клавишу для продолжения.")
    stdscr.refresh()
    stdscr.getch()



def mark_task_as_done(stdscr, task_list):
    stdscr.clear()
    stdscr.addstr("Отметить задачу как выполненную\n\n")
    stdscr.addstr("Введите номер задачи: ")
    index = get_numeric_input(stdscr) - 1
    task = task_list.get_task(index)
    if task:
        task.mark_as_done()
        stdscr.addstr("Задача успешно отмечена как выполненная. Нажмите любую клавишу для продолжения.")
    else:
        stdscr.addstr("Задача не найдена. Нажмите любую клавишу для продолжения.")
    stdscr.refresh()
    stdscr.getch()


def remove_task(stdscr, task_list):
    stdscr.clear()
    stdscr.addstr("Удаление задачи\n\n")
    stdscr.addstr("Введите номер задачи(если хотите удалить все задачи введите 0): ")
    index = get_numeric_input(stdscr) - 1
    task = task_list.get_task(index)
    if task:
        task_list.remove_task(index)
        stdscr.addstr("Задача успешно удалена. Нажмите любую клавишу для продолжения.")
    else:
        stdscr.addstr("Задача не найдена. Нажмите любую клавишу для продолжения.")
    stdscr.refresh()
    stdscr.getch()


def main(stdscr):
    task_list = TaskList()
    task_list.load_from_json()
    
    while True:
            print_tasks(stdscr, task_list)
            stdscr.addstr("\nВыберите действие:\n")
            stdscr.addstr("1. Создать задачу\n")
            stdscr.addstr("2. Отметить задачу как выполненную\n")
            stdscr.addstr("3. Удалить задачу\n")
            stdscr.addstr("4. Подробная информация\n")
            stdscr.addstr("5. Выход\n")
            stdscr.addstr("Ваш выбор: ")
            stdscr.refresh()
            choice = stdscr.getstr().decode()
            if choice == '1':
                create_task(stdscr, task_list)
            elif choice == '2':
                mark_task_as_done(stdscr, task_list)
            elif choice == '3':
                remove_task(stdscr, task_list)
            elif choice == '4':
                info_tasks(stdscr, task_list)
            elif choice == '5':
                break

        # Сохранение данных в JSON перед выходом
    task_list.save_to_json()

    # Завершение работы с curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    stdscr = initialize_screen()
    curses.wrapper(main)