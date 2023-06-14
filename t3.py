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
        return f'{self.name} - {self.des}\nCurrently isdone -> {self.status}'


class TaskList:
    ls = []


    def create_task(self, name, des, date, status=False):
        for i in self.ls:
            if name == i['name']:
                return 'Already exists'
        self.ls.append(
            {'name': name, 'description': des, 'date': date, 'status': status}
        )
        return 'Created'

    def get_task(self, search):
        for i in self.ls:
            if search == i['name']:
                return i
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
    