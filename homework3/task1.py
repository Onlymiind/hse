items = {
    'milk15':{'name': 'молоко 1.5%', 'count': 34, 'price': 89.9},
    'cheese':{'name': 'сыр молочный 1 кг.', 'count': 12, 'price': 990.9},
    'sausage':{'name': 'колбаса 1 кг.', 'count': 122, 'price': 1990.9}
}

count_lt_20 = {key: items[key]['count'] < 20 for key in items.keys()}
print(count_lt_20)