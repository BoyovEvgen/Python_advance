class Profile:
    """
    Create regular class taking 8 params on init -
    name, last_name, phone_number, address, email, birthday, age, sex.
    Override a printable string representation of Profile class and return:
    list of the params mentioned above
    """
    def __init__(self, name, last_name, phone_number, address, email, birthday, age, sex):
        self.name = name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.email = email
        self.birthday = birthday
        self.age = age
        self.sex = sex

    def __str__(self):
        return str(list(self.__dict__))


if __name__ == '__main__':
    user = Profile('Evhen', 'Boiov', '+38078946512',
                   'Dnipro', 'e.boyov@gmail.com', '01.01.23', 30, 'man')
    print(user)
