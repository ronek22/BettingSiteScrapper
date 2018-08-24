from core.constants import MENU_TEXT
from core.fortuna import Fortuna
from core.utility import choose_user
from analysis.user import User
import os


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
        site.get_deposits()
        site.close()

    @staticmethod
    def run_analysis():
        user = User(*choose_user(), True)
        os.system('cls')
        user.show_data()


    def menu(self):
        menu_options = [self.perform_scraping, self.run_analysis, self.close_program]
        while True:
            os.system('cls')
            print(MENU_TEXT)
            choose = int(input("> "))
            os.system('cls')
            if 1 <= choose <= len(menu_options):
                menu_options[choose - 1]()
                input("Click any key to continue...")
            else:
                print("That option doesn't exist. Try again")