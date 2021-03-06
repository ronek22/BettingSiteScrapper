from selenium import webdriver
from core.bookies.fortuna.pages import *
from core.utility import sorting_json, save_to_json, open_json
from os.path import isfile


class Fortuna:
    def __init__(self):
        self.user = (input("User: "), input("Password: "))
        self.history_name = 'history_' + self.user[0] + '.json'
        self.deposits_name = 'deposits_' + self.user[0] + '.json'

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('window-size=1400,1200')
        self.driver = webdriver.Chrome(executable_path='drivers/chromedriver.exe', chrome_options=options)
        self.driver.get("https://www.efortuna.pl")
        self.bet_list = []
        self.deposit_list = []

    def login(self):
        page = LogInPage(self.driver)
        page.login(self.user[0], self.user[1])

    def get_deposits(self):
        page = DepositsPage(self.driver)
        self.deposit_list = page.scrap_deposits_data()
        save_to_json(self.deposit_list, self.deposits_name)

    def get_history(self):
        last_date = None
        if isfile('history/' + self.history_name):
            self.bet_list = open_json(self.history_name)
            last_date = self.bet_list[0]['date']

        self.get_all_bets(last_date)
        save_to_json(sorting_json(self.bet_list), self.history_name)

    def get_all_bets(self, date=None):
        page = BetHistoryPage(self.driver)
        page.go_to_pre_match_bets()
        self.loop_bets(date)
        page.go_to_live_bets()
        self.loop_bets(date)

    def loop_bets(self, date=None):
        # TODO: Too complex method, try to divide it
        detail = BetDetailPage(self.driver)

        while detail.still_have_bets():
            num_of_bets = detail.click_on_first_bet()
            detail.switch_to_bet_iframe()
            print('Number of bets:' + str(num_of_bets))
            for bet in range(0, num_of_bets):
                bet_details = detail.scrap_details_about_bet()

                if (date is not None and bet_details['date'] > date) or date is None:
                    self.bet_list.append(bet_details)
                else:
                    return 0

                if num_of_bets != 1: detail.get_next_bet()
            detail.get_next_page()

    def close(self):
        self.driver.close()
