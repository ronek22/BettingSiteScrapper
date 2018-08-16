from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from core.pages import *
import json


class Fortuna:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='drivers/geckodriver.exe')
        self.driver.get("https://www.efortuna.pl")
        self.wait = WebDriverWait(self.driver, 60)
        self.bet_list = []

    def login(self):
        page = LogInPage(self.driver)
        print('Please fill you credentials to efortuna.pl site.')
        user, password = input("User: "), input("Password: ")
        page.login(user, password)

    def get_history(self):
        page = BetHistoryPage(self.driver)

        page.go_to_pre_match_bets()
        self.loop_bets()
        page.go_to_live_bets()
        self.loop_bets()

        self.save_to_json()
        self.driver.close()

    def loop_bets(self):
        detail = BetDetailPage(self.driver)

        while detail.still_have_bets():
            num_of_bets = detail.click_on_first_bet()
            detail.switch_to_bet_iframe()
            print('Number of bets:' + str(num_of_bets))
            for bet in range(0, num_of_bets):
                self.bet_list.append(detail.scrap_details_about_bet())
                if num_of_bets != 1:
                    detail.get_next_bet()
            detail.get_next_page()

    def save_to_json(self):
        with open('bettingHistory.json', 'w') as outfile:
            json.dump(self.bet_list, outfile, indent=4)




