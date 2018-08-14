from core.base import Page
from core.locators import *
import re
from datetime import datetime


class LogInPage(Page):
    def __init__(self, driver):
        self.locator = LoginPageLocators
        super().__init__(driver, 'https://www.efortuna.pl/')

    def enter_login(self, user):
        self.find_element(*self.locator.LOGIN).send_keys(user)

    def enter_password(self, password):
        self.find_element(*self.locator.PASSWORD).send_keys(password)

    def click_login_button(self):
        self.find_element(*self.locator.PASSWORD).submit()

    def login(self, user, password):
        self.enter_login(user)
        self.enter_password(password)
        self.click_login_button()
        self.wait_for_url(self.base_url + '?log=success')


class BetHistoryPage(Page):
    def __init__(self, driver):
        super().__init__(driver, 'https://www.efortuna.pl/pl/profil_uzytkownika/zaklady/')
        self.open()

    def go_to_pre_match_bets(self):
        return self.open('przeglad_zakladow/index.html?offset=0')

    def go_to_live_bets(self):
        return self.open('przeglad_zakladow_live/index.html?offset=0')


class BetDetailPage(Page):
    def __init__(self, driver):
        self.locator = BetDetailLocators
        self.offset = 30
        super().__init__(driver, 'https://www.efortuna.pl/pl/profil_uzytkownika/zaklady/')

    def scrap_details_about_bet(self):
        summary = self.wait_for_element(*self.locator.SUMMARY)

        self.get_general_info(summary)

        bet_summary = {
            'date': self.get_date_and_convert(summary),
            'live': self.check_if_live()
        }

        bet_summary.update(self.get_general_info(summary))
        bet_summary['events'] = self.get_events_from_bet(),
        return bet_summary

    def get_general_info(self, summary):
        table = summary.find_element(By.TAG_NAME, 'tbody')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        return {
            'total_odds': float(self.strtfloat(rows[0].text)),
            'stake': self.strtfloat(rows[3].text),
            'stake_after_taxes': self.strtfloat(rows[1].text),
            'payout': self.strtfloat(rows[4].text)}

    def get_date_and_convert(self, summary):
        bottom_info = summary.find_element(*self.locator.BOTTOM_INFO)
        date_str = bottom_info.find_elements(By.TAG_NAME, 'div')[3].text
        date_str = re.sub('[^\d\.\:]', '', date_str)[1:]
        date = datetime.strptime(date_str, '%d.%m.%Y%H:%M:%S')
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def get_events_from_bet(self):
        table = self.wait_for_element(*self.locator.TICKET_TABLE)
        bets = table.find_elements(*self.locator.BETS_IN_TABLE)

        events = []

        for bet in bets:
            event_detail = {
                'name': bet.find_element(*self.locator.BET_NAME).text,
                'selection': bet.find_element(*self.locator.BET_TYPE).text,
                'type': bet.find_elements(By.TAG_NAME, 'td')[1].text.strip(),
                'odds': float(bet.find_element(*self.locator.BET_ODDS).text),
                'result': bet.find_element(*self.locator.BET_RESULT).text.strip(),
                'win': self.is_winner(bet.get_attribute("class"))}
            events.append(event_detail)
        return events

    @staticmethod
    def is_winner(css_name):
        return 'Y' if 'non_winning' not in css_name else 'N'

    @staticmethod
    def strtfloat(text):
        return re.sub('[^\d\.]', '', text)

    def get_next_bet(self):
        self.driver.switch_to.default_content()
        next_button = self.wait_for_element(*self.locator.NEXT_BET)
        next_button.click()
        self.switch_to_bet_iframe()

    def still_have_bets(self):
        return False if "Brak kupo" in self.driver.page_source else True

    def check_if_live(self):
        return 'Y' if "LIVE" in self.driver.page_source else 'N'

    def get_next_page(self):
        url = re.sub(r'\d+$', '', self.get_url())
        self.driver.get(url + str(self.offset))
        self.offset += 30

    def click_on_first_bet(self):
        bets = self.find_elements(*self.locator.FIRST_BET)
        bets[0].click()
        return len(bets)

    def switch_to_bet_iframe(self):
        iframe = self.wait_for_element(*self.locator.FRAME_DETAIL_BET)
        self.driver.switch_to_frame(iframe)