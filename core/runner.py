from core.constants import MENU_TEXT
from core.bookies.fortuna.fortuna import Fortuna
from core.utility import choose_user, get_user, send_to_discord
from analysis.user import User
import os


class Runner:
    def __init__(self, log, pswd):
        self.login = log
        self.password = pswd
        self.run()

    def perform_scraping(self):
        site = Fortuna(self.login, self.password)
        site.login()
        site.get_history()
        site.get_deposits()
        site.close()

    def run_analysis(self):
        user = User(*get_user(self.login), True)
        return user.get_data()

    def run(self):
        """For automation"""
        self.perform_scraping()
        analysis = self.run_analysis()
        send_to_discord(self.login, analysis)
        exit(0)
