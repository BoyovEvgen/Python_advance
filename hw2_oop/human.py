from realtor import Realtor


class Human:
    def __init__(self, name, age, money=0, house=None):
        self.name = name
        self.age = age
        self.__money = money
        self.__house: list = []
        self.promocode = None
        if house:
            self.__house.append(house)

    def get_info(self):
        return {'name': self.name,
                'age': self.age,
                'money': self.__money,
                'house': self.__house}

    def make_money(self):
        self.__money += 10

    def give_money(self, sum_money):
        self.__money -= sum_money
        return sum_money

    def choose_house(self):
        print("Виберіть будинок:")

        houses = Realtor().get_list_sales()
        for house in houses.values():
            print(house)
        num_house = int(input(" Введіть номер обраного будинку: "))
        print('=============================\n')
        return num_house

    def bay_house(self):
        money_at_the_beginning = self.__money
        num_house = self.choose_house()
        try:
            house = Realtor().sell_house(buyer=self, id_house=num_house, promocode=self.promocode)
            if house:
                self.__house.append(house)
                print('ВІТАЮ УГОДА ПРОЙШЛА УСПІШНО!')
                print(f'Будинок {self.__house[-1]} куплено!')

            elif money_at_the_beginning != self.__money:
                print(f"Ріэлтор вкрав гроші!! Було грошей {money_at_the_beginning}, лишилось {self.__money}")

        except ValueError as refusal:
            print(refusal)

        except Exception as revert:
            print(revert)
            if money_at_the_beginning != self.__money:
                self.__money = money_at_the_beginning

    def ask_discount(self):
        self.promocode = Realtor().give_discount()
        print('Ти отримав скидку 5 умовних одиниць на всі будинки')

