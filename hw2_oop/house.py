from realtor import Realtor


class House:
    __last_id = 0

    def __init__(self, price, area=40):
        self.area = area
        self.price = price
        self.unique_id = self.__set_unique_id()
        self.put_up_for_sales()

    @classmethod
    def __set_unique_id(cls):
        house_id = cls.__last_id + 1
        cls.__last_id = house_id
        return house_id

    def put_up_for_sales(self):
        Realtor().take_for_sale(house=self)

    def __repr__(self):
        return f"House num {self.unique_id} площею {self.area} з ціною {self.price} без урахування знижок."
