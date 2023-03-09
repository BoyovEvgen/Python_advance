from human import Human
from realtor import Realtor
from house import House


def input_int(massege=''):
    try:
        res = int(input(massege))
        return res
    except ValueError:
        print('Треба ввести чило')
        input_int(massege)


realtor = Realtor()
house40m = House(price=80)
House80m = House(price=120, area=80)
House85m = House(price=130, area=85)

name = input('Введіть Ваше імʼя: ')
age = input_int('Скільки Вам років?: ')
human = Human(name=name, age=age, money=60,)

while True:
    print("Що бажаєте зробити?",
          "1. Переглянути будинки на продажі",
          "2. Порахувати мої гроші",
          "3. Заробити грошей",
          "4. Попросити знижку",
          "5. Придбати будинок",
          "6. Переглянути властні будинки",
          "7. Створити ще будинки",
          "exit Завершити",
          sep="\n")
    choose = input("Введіть номер дії, або введіть exit для виходу: ")
    print('=============================\n')

    match choose:
        case '1':
            print('Будинки для продажу')
            houses = realtor.get_list_sales()
            for house in houses.values():
                print(house)
            print('=============================\n')
        case '2':
            print(human.get_info()['money'], ' умовних одиниць', '\n=============================\n')
        case '3':
            human.make_money()
            print('Ти попрацював і заробив 10 умовних одиниць')
            print('=============================\n')
        case '4':
            human.ask_discount()
            print('=============================\n')
        case '5':
            human.bay_house()
            print('=============================\n')
        case '6':
            print(f'{human.name} maє у властності {human.get_info()["house"]}')
            print('=============================\n')
        case '7':
            area = input_int('Якою площею буде новий будинок? ')
            price = input_int('Яка буде ціна? ')
            House(price, area)
            print('Побудовано ноий будинок')
            print('=============================\n')
        case 'exit':
            break
        case _:
            print('Невідома команда, зробіть ще раз вибор...')
            print('=============================\n')







