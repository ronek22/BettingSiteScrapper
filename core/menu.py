from core.constants import MENU_TEXT
from core.fortuna import Fortuna
from transform import run_analysis


class Menu:
    def __init__(self):
        self.menu()

    @staticmethod
    def close_program():
        print("Thank you, see you later")
        exit(0)

    @staticmethod
    def perform_scraping():
        site = Fortuna()
        site.login()
        site.get_history()

    def menu(self):
        menu_options = [self.perform_scraping, run_analysis, self.close_program]
        while True:
            print(MENU_TEXT)
            choose = int(input("> "))
            if 1 <= choose <= len(menu_options):
                menu_options[choose - 1]()
                input("Click any key to continue")
            else:
                print("That option doesn't exist. Try again")