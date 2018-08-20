from core.base import Page
from core.constants import sports
from core.locators import *
import re
from datetime import datetime

from core.utility import str_to_float


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


class DepositsPage(Page):
    def __init__(self, driver):
        super().__init__(driver, 'https://www.efortuna.pl/pl/profil_uzytkownika/user_profile/bilans_konta/')
        self.locator = DepositsPageLocators
        self.open()

    def select_deposit_filter(self, value):
        form = self.wait_for_element(*self.locator.FORM)
        self.select_from_dropdown(value, *self.locator.TYPE_OF_TRANSACTION)
        form.submit()

    def scrap_deposits_data(self):
        self.select_deposit_filter('wpłata - przelew bankowy')
        table = self.wait_for_element(*self.locator.TABLE)
        deposits = table.find_elements(*self.locator.DEPOSITS_IN_TABLE)[1:]

        result = []

        for deposit in deposits:
            deposit_detail = {
                'value': float(str_to_float(deposit.find_element(*self.locator.CASH).text)),
                'transaction_number': deposit.find_element(*self.locator.NUMBER).text,
                'date': deposit.find_element(*self.locator.DATE).text.replace('  ', ' ')
            }
            result.append(deposit_detail)
        return result


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
            'live': self.check_if_live(),
        }

        bet_summary.update(self.get_general_info(summary))
        bet_summary['events'] = self.get_events_from_bet()
        return bet_summary

    def get_general_info(self, summary):
        table = summary.find_element(By.TAG_NAME, 'tbody')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        total_odds = float(str_to_float(rows[0].text))
        stake = float(str_to_float(rows[3].text))
        stake_after_taxes = float(str_to_float(rows[1].text))
        payout = float(str_to_float(rows[4].text))

        # TODO: Probably not working with additional taxes
        return {
            'total_odds': total_odds,
            'stake': stake,
            'stake_after_taxes': stake_after_taxes,
            'potential_payout': float("{0:.2f}".format(stake_after_taxes*total_odds)),
            'payout': payout,
            'status': self.bet_status(payout)
        }

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
                'selection': bet.find_element(*self.locator.BET_TYPE).text.strip(),
                'type': bet.find_elements(By.TAG_NAME, 'td')[1].text.strip(),
                'odds': float(bet.find_element(*self.locator.BET_ODDS).text),
                'result': bet.find_element(*self.locator.BET_RESULT).text.strip(),
                'win': self.is_winner(bet.get_attribute("class"))}
            event_detail.update(self.process_bet_title(bet.find_element(*self.locator.BET_NAME).text))
            events.append(event_detail)
        return events

    def process_bet_title(self, title):
        title = title.split(' - ')
        title_len = len(title)
        bet = dict()

        if title[0][0].isupper():
            if title_len == 3:
                bet = {'sport': title[0], 'league': title[1], 'name': title[2]}
            elif title[0] == 'Lekkoatletyka':
                bet = {'sport': title[0], 'league': '', 'name': title[2] + ' - ' + title[1]}
            elif title[0] == 'HIT DNIA':
                bet = {'sport': self.parse_sport(title[1]), 'league': '', 'name': title[2] + ' - ' + title[3]}
            elif title[0] == 'Piłka nożna-MS 2018':
                bet = {'sport': self.parse_sport(title[0])[0], 'league': self.parse_sport(title[0])[1], 'name': title[2] + ' - ' + title[3]}
            elif title_len == 4:
                bet = {'sport': self.parse_sport(title[0]), 'league': title[1], 'name': title[2] + ' - ' + title[3]}
            elif title_len == 5:
                bet = {'sport': self.parse_sport(title[0]), 'league': title[1] + ' - ' + title[2], 'name': title[2] + ' - ' + title[3]}
        else:
            # live bets is not capitalized
            if title_len == 4:
                bet = {'sport': self.parse_sport(title[0]), 'league': self.parse_sport(title[1]), 'name': title[2] + ' - ' + title[3]}
            elif title_len == 5:
                bet = {'sport': self.parse_sport(title[0]), 'league': title[1] + ' - ' + title[2], 'name': title[3] + ' - ' + title[4]}
            elif title_len == 6:
                bet = {'sport': self.parse_sport(title[0]), 'league': title[1] + ' - ' + title[2], 'name': title[4] + ' - ' + title[5]}
        return bet

    @staticmethod
    def parse_sport(title):
        value = ''
        try:
            value = sports[title]
        except KeyError:
            value = title
        finally:
            return value

    @staticmethod
    def is_winner(css_name):
        if 'non_winning' in css_name:
            return 'N'
        elif 'unresolved' in css_name:
            return 'P'
        else:
            return 'Y'

    def get_next_bet(self):
        self.driver.switch_to.default_content()
        next_button = self.wait_for_element(*self.locator.NEXT_BET)
        next_button.click()
        self.switch_to_bet_iframe()

    def still_have_bets(self):
        return False if "Brak kupo" in self.driver.page_source else True

    def bet_status(self, payout):
        if "Kupon jest już rozs" in self.driver.page_source:
            return 'W' if payout > 0 else "L"
        else:
            return "P"

    def check_if_live(self):
        return 'Y' if "LIVE" in self.driver.page_source else 'N'

    def get_next_page(self):
        url = re.sub(r'\d+$', '', self.get_url())
        self.driver.get(url + str(self.offset))
        print('Opening: ' + url)
        self.offset += 30

    def click_on_first_bet(self):
        bets = self.find_elements(*self.locator.FIRST_BET)
        bets[0].click()
        return len(bets)

    def switch_to_bet_iframe(self):
        iframe = self.wait_for_element(*self.locator.FRAME_DETAIL_BET)
        self.driver.switch_to_frame(iframe)