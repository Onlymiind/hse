from datetime import datetime

def parse_date(date_str, format):
    try:
        return datetime.strptime(date_str, format)
    except:
        return None

def get_date_str():
    str = input('Enter date or \'q\' to exit\n')
    if str == 'q':
        return None
    return str

formats = ['%A, %B %d, %Y', '%A, %d.%m.%y', '%A, %d %B %Y']

date = get_date_str()
while date != None:
    success = False
    for fmt in formats:
        print(fmt)
        parsed = parse_date(date, fmt)
        if parsed != None:
            success = True
            print(parsed)
            break
    if not success:
        print('Format not recognized\n')
    date = get_date_str()
