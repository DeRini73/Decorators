import os
from datetime import datetime
import time


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            start = datetime.now()
            start_formatted = f"{start.day:02d}.{start.month:02d}.{start.year} в {start.hour:02d} ч {start.minute:02d} мин {start.second:02d} с"

            function_name = old_function.__name__
            result = old_function(*args, **kwargs)

            args_repr = [repr(a) for a in args]
            kwargs_repr = [f'{k}={repr(v)}' for k, v in kwargs.items()]
            all_args = ", ".join(args_repr + kwargs_repr)

            time.sleep(1)

            log = (f'{start_formatted} была вызвана функция "{function_name}" с аргументами "{all_args}". Результат выполнения функции: {result}\n')

            with open(path, 'a',encoding='utf-8') as log_file:
                log_file.write(log)

            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        @logger(path)
        def calculate_salary():
            return ('Расчет заработной платы за текущий период выполнен.'
                    'Всё очень печально, главбух сбежал.'
                    'Её так и не нашли')

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)
        result = calculate_salary()
        assert ('Расчет заработной платы за текущий период выполнен.'
                'Всё очень печально, главбух сбежал.'
                'Её так и не нашли'
                in result), "Функция calculate_salary должна вернуть строку"


    for path in paths:


        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'
        assert 'calculate_salary' in log_file_content, 'должно записаться имя функции'
        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
