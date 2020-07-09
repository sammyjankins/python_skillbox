# -*- coding: utf-8 -*-

# Написать декоратор, который будет логировать (записывать в лог файл)
# ошибки из декорируемой функции и выбрасывать их дальше.
#
# Имя файла лога - function_errors.log
# Формат лога: <имя функции> <параметры вызова> <тип ошибки> <текст ошибки>
# Лог файл открывать каждый раз при ошибке в режиме 'a'

from functools import wraps


def log_errors(file_name):
    def logging_wrapper(func):
        @wraps(func)
        def surrogate(*args, **kwargs):
            divider = '------------------------------------------------------------------------\n'
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                with open(file_name, mode='a', encoding='utf8') as log:
                    err_type = exc.__class__.__name__
                    # не определился как лучше, извлекать из скобок или записывать в исходном виде
                    # args_line = f' с параметрами: {", ".join(map(str, args))}' if args else ''
                    args_line = f' с параметрами: {args}' if args else ''
                    if kwargs:
                        kwargs_line = (f' с именованными параметрами: '
                                       f'{", ".join([f"{key}={value}" for key, value in kwargs.items()])}')
                    else:
                        kwargs_line = ''
                    log.write(f'Исполнение функии {func.__name__}{args_line}'
                              f'{"," if args and kwargs else ""}{kwargs_line}\n'
                              f'привело к ошибке типа {err_type} - {exc}\n{divider}')
                raise exc

        return surrogate

    return logging_wrapper


# Проверить работу на следующих функциях
@log_errors('function_errors.log')
def perky(param):
    """Делю на ноль, потому что могу!
    Или не могу...
    """
    return param / 0


@log_errors('function_errors.log')
def check_line(line):
    """Проверяю корректность данных регистрации
    """
    name, email, age = line.split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not a email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]
for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')
perky(param=42)

# Усложненное задание (делать по желанию).
# Написать декоратор с параметром - именем файла
#
# @log_errors('function_errors.log')
# def func():
#     pass
