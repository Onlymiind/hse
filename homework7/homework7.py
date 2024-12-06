class Person:
    def __init__(self, name, sex, age, device_type, browser, bill, region):
        self.name = name
        self.age = float(age)
        self.device_type = device_type
        self.browser = browser
        self.bill = float(bill)
        self.region = region
        if sex == 'female':
            self.sex = True
        else:
            self.sex = False

    def __str__(self):
        format = 'Пользователь {} {} пола, {:g} лет {} покупку на {:g} у.е. с {} браузера {}. Регион, из которого совершалась покупка: {}.'
        sex = ''
        action = ''
        if self.sex:
            sex = 'женского'
            action = 'совершила'
        else:
            sex = 'мужского'
            action = 'совершил'
        device_type = ''
        if self.device_type in {'mobile', 'tablet'}:
            device_type = 'мобильного'
        elif self.device_type in {'desktop', 'laptop'}:
            device_type = 'десктопного'
        else:
            device_type = 'неопределенного'
        return format.format(self.name, sex, self.age, action, self.bill, device_type, self.browser, self.region)


def process_data(src_file, dst_file):
    # skip the header row
    src_file.readline()
    for line in src_file:
        fields = line.split(',')
        if len(fields) < 7:
            continue
        person = Person(fields[0].strip(), fields[3].strip(), fields[4], fields[1].strip(), fields[2].strip(), fields[5], fields[6].strip())
        dst_file.write(str(person))
        dst_file.write('\n')

src = open('web_clients_correct.csv', 'r')
dst = open('web_clients.txt', 'w')

process_data(src, dst)

