import random
import string


class Realtor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if '_cash' not in self.__dict__:
            self._cash = 0
            self.list_sales_houses = {}  # id:<instance House>
            self.__promocode = ''
        # print(self.__dict__)

    def take_for_sale(self, house):
        self.list_sales_houses[house.unique_id] = house

    def get_list_sales(self):
        return self.list_sales_houses

    def take_money(self, buyer, price):
        self._cash += buyer.give_money(sum_money=price)
        return True

    @staticmethod
    def __deceive():
        # if random.randint(0, 10) == 0:
        if random.randint(0, 2) == 0:  # збільшив імовірність обману, щоб скоріше настав такий випадок - для тестування
            return True

    def sell_house(self, buyer, id_house, promocode):
        price = self.__get_discounted_price(id_house, promocode)
        if buyer.get_info()['money'] >= price:
            if self.take_money(buyer, price):
                if self.__deceive():
                    return
                return self.list_sales_houses.pop(id_house)
            else:
                raise Exception("The deal fell through")
        else:
            raise ValueError("Sorry, you don't have enough money")

    def give_discount(self):
        charstr = string.ascii_letters + string.digits
        self.__promocode = ''.join([random.choice(charstr) for _ in range(8)])
        return self.__promocode

    def __get_discounted_price(self, id_house, promocode):
        price = self.list_sales_houses[id_house].price
        if promocode == self.__promocode:
            price -= 5
        return price



