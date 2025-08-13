import csv

animals = {
    15: 'Raposa',
    14: 'Lobo',
    3: 'Elefante',
    6: 'Urso',
    20: 'Koala',
    11: 'Jacaré',
    2: 'Tigre',
    17: 'Coruja',
    9: 'Golfinho',
    10: 'Tubarão',
    18: 'Gorila',
    5: 'Zebra',
    13: 'Hipopótamo',
    19: 'Chimpanzé',
    1: 'Leão',
    7: 'Canguru',
    8: 'Pinguim',
    4: 'Girafa',
    16: 'Águia',
    12: 'Rinoceronte'
}

animals_sort = sorted(animals.items())

for i in animals_sort:
    print(i)

with open('animals.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Id', 'Animais'])
    for k, v in animals_sort:
        writer.writerow([k, v])







