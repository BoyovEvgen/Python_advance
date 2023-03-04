from abc import ABC, abstractmethod


class Laptop(ABC):
    """ Create an interface for the Laptop with the next methods:
    Screen, Keyboard, Touchpad, WebCam, Ports, Speaker.
    create an HPLaptop class by using your interface."""
    @abstractmethod
    def screen(self):
        pass

    @abstractmethod
    def keyboard(self):
        pass

    @abstractmethod
    def touchpad(self):
        pass

    @abstractmethod
    def webCam(self):
        pass

    @abstractmethod
    def ports(self):
        pass

    @abstractmethod
    def speaker(self):
        pass


class HPLaptop(Laptop):
    def screen(self):
        print('HPLaptops screen shows')

    def keyboard(self):
        print('keyboard working')

    def touchpad(self):
        print('touchpad working')

    def webCam(self):
        print('webCam working')

    def ports(self):
        print('ports working')

    def speaker(self):
        print('speaker working')


if __name__ == '__main__':
    hp = HPLaptop()
    hp.screen()
