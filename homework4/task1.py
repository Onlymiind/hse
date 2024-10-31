def search(collection, predicate):
    for val in collection:
        if predicate(val):
            return val
    return None

def find_owner(documents, doc_number):
    doc = search(documents, lambda val: True if val['number'] == doc_number else False)
    if doc != None:
        return doc['name']
    else:
       return 'владелец не найден'

def find_directory(directories, doc_number):
    directory = search(directories, lambda dir: search(directories[dir], lambda num: True if num == doc_number else False) != None)
    if directory != None:
        return directory
    else:
        return 'дt aокумент не найден'

def read_command():
    return input('Введите команду:\n')

def read_document_number():
    return input('Введите номер документа:\n');

def main_loop():
    command = read_command()
    while command != 'q':
        if command == 'p':
            print('Владелец документа: ' + find_owner(documents, read_document_number()))
        elif command == 's':
            print('Документ хранится на полке: ' + find_directory(directories, read_document_number()))
        else:
            print('Неизвестная команда!\n')
        command = read_command()

documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

main_loop()
