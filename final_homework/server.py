from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
import sys
import json
import time

class Task:
    def __init__(self, title, priority, isDone, id):
        # Инициализация задачи, валидация параметров
        self.title = title
        priority = priority.strip()
        if priority not in {'low', 'normal', 'high'}:
            raise ValueError(f'priority must be one of "low", "normal", "high", got "{priority}"')
        self.priority = priority
        if not isinstance(isDone, (bool)):
            raise TypeError('isDone must be a boolean')
        elif not isinstance(id, (int)):
            raise TypeError('id nust be an integer')
        self.isDone = isDone
        self.id = id

    def __str__(self):
        # В задаче не указан конкретный формат сохранения задач в файл, поэтому
        # я выбрал CSV-подобный
        return f'{self.title},{self.priority},{self.isDone:0},{self.id}'

    # Возвращает репрезентацию задачи в виде словаря для сериализации задачи в JSON
    def json_value(self):
        return {'title':self.title,
                'priority':self.priority,
                'isDone':self.isDone,
                'id':self.id}

    # Устанавливает isDone = True
    def mark_completed(self):
        self.isDone = True

# Создает задачу из строки (для формата см. Task.__str__).
# Если формат некорректен, возвращает None
def parse_task(string):
    values = [piece.strip() for piece in string.split(',')]
    if len(values) < 4:
        return None
    elif values[2] not in {'0', '1'}:
        return None
    elif values[1] not in {'low', 'normal', 'high'}:
        return None
    id = 0
    try:
        id = int(values[3])
    except ValueError:
        return None
    return Task(values[0], values[1], True if values[2] == '1' else False, id)

# Считывает все задачи из файла.
# При возникновении ошибок пропускает проблемную строку в файле и выводит соответствующее сообщение
def read_tasks(filepath):
    result = {}
    try:
        file = open(filepath, 'r')
    except:
        # Файла нет, вернуть пустой словарь
        return result
    for line in file.readlines():
        # Парсинг задачи
        task = parse_task(line)
        if task == None:
            # Ошибка парсинга
            print(f'failed to parse task from line: "{line}"')
            continue
        # Сохранить задачу в результат
        result[task.id] = task
    file.close()
    # Вернуть результат
    return result

# Специализвация json.JSONEncoder, поддерживающая сериализацию задач
class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Task)):
            return obj.json_value()
        return super().default(obj)


class Handler(BaseHTTPRequestHandler):
    def __init__(self, tasks, filepath, *args):
        self.tasks = tasks
        self.filepath = filepath
        if not tasks:
            self.current_id = 0
        else:
            self.current_id = max(tasks.keys())
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        # Проверка корректности пути запроса
        if not self.path == '/tasks':
            print('unknown path')
            self.send_response(404)
            self.end_headers()
            return
        # Отправить в ответе все задачи, сериализованные в JSON
        print('sending all tasks')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(TaskEncoder().encode(list(self.tasks.values())).encode())

    def do_POST(self):
        path = self.path.split('/')
        if self.path == '/tasks':
            # Добавление новой задачи
            self.add_task()
        elif len(path) == 4 and path[1] == 'tasks' and path[3] == 'complete':
            # Возможно, это запрос на отметку о выполеннии задачи
            try:
                id = int(path[2])
                # Отметить задачу как выполненную или вернуть 404
                self.complete_task(id)
            except ValueError:
                # Нет, т.к. второй элемент пути должен быть целым числом
                print(f'second element of path "{self.path}" is not an integer')
                self.send_response(400)
                self.end_headers()
        else:
            # Неизвестный путь запроса
            print('unknown path')
            self.send_response(404)
            self.end_headers()

    def add_task(self):
        print('adding new task')
        try:
            # Считать тело запроса
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length)
            print('parsing request body as JSON')
            task_json = json.loads(body)

            # Получить следующий идентификатор и создать новую задачу
            self.current_id += 1
            task = Task(task_json["title"], task_json["priority"], False, self.current_id)
            self.tasks[task.id] = task
            print('new task successfully created')

            # Сохранить задачи в файл
            self.write_tasks()
            print('sending response')

            # Отправить ответ
            self.send_response(200)
            self.end_headers()
        except (ValueError, KeyError):
            # Некорректный JSON, некорректные значения атрибутов, отсутствие атрибутов
            print('request for adding a task has invalid body')
            self.send_response(400)
            self.end_headers()
        except Exception as e:
            # Внутренняя ошибка сервера
            print(f'got an unexpected exception: {e}')
            self.send_response(500)
            self.end_headers()

    def complete_task(self, id):
        if not id in self.tasks:
            # Задача не найдена, отправить 404
            print(f'task {id} not found')
            self.send_response(404)
            self.end_headers()
            return

        # Отметить задачу как выполненную
        print(f'marking task {id} as completed')
        self.tasks[id].mark_completed()

        # Задачи были изменены, сохранить их на диск
        self.write_tasks()
        print('sending response')

        # Отправить ответ
        self.send_response(200)
        self.end_headers()

    def write_tasks(self):
        print('saving tasks to temporary file')
        # Сначала записать задачи во временный файл, чтобы не повредить
        # валидные данные в выходном файле
        name = f'{self.filepath}_temp{time.time_ns()}.txt'
        temp = open(name, 'w')

        # Записать все задачи
        for task in self.tasks.values():
            temp.write(f'{task}\n')
        print('tasks saved, renaming the file')
        temp.close()

        # Переименовать временный файл
        os.rename(name, self.filepath)

def run():
    filepath = ''
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'output.txt'

    # Считать все задачи из файла, если он есть
    tasks = read_tasks(filepath)
    
    # Создает инстанс хэндлера запросов
    def make_handler(*args):
        return Handler(tasks, filepath, *args)

    # Запуск сервера
    httpd = HTTPServer(('', 8080), make_handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

run()
