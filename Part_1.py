import os
from datetime import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        start = datetime.now()
        start_formatted = f"{start.day:02d}.{start.month:02d}.{start.year} в {start.hour:02d} ч {start.minute:02d} мин"

        function_name = old_function.__name__
        result = old_function(*args, **kwargs)

        args_str = ', '.join([str(arg) for arg in args])
        kwargs_str = ', '.join([f'{key}:{value}' for key, value in kwargs.items()])

        all_args = args_str
        if kwargs_str:
            if args_str:
                all_args += ', ' + kwargs_str
            else:
                all_args = kwargs_str

        log = (f'{start_formatted} была вызвана функция "{function_name}" с аргументами "{all_args}". Результат выполнения функции: {result}\n')

        with open('main.log', 'a', encoding='utf-8') as log_file:
            log_file.write(log)

        return result

    return new_function

print(f'Результат сохранен в файле "main.log"')

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()