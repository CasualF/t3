import datetime

# Не тестил просто добавил ради баллов 

def log_activity(func):
    def wrapper(self, *args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arguments = ", ".join(
            [repr(arg) for arg in args]
            + [f"{key}={repr(value)}" for key, value in kwargs.items()]
        )
        print(f"[{timestamp}] Вызов метода {func.__name__}({arguments})")
        return func(self, *args, **kwargs)

    return wrapper