from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN = (By.NAME, 'login')
    PASSWORD = (By.NAME, 'password')


class BetDetailLocators:
    FIRST_BET = (By.CLASS_NAME, 'ticket_origin')
    FRAME_DETAIL_BET = (By.ID, 'shadowbox_content')
    TICKET_TABLE = (By.CLASS_NAME, 'ako')
    BETS_IN_TABLE = (By.TAG_NAME, 'tr')
    BET_NAME = (By.CLASS_NAME, 'bet_item_name')
    BET_TYPE = (By.CLASS_NAME, 'matchComment')
    BET_ODDS = (By.CLASS_NAME, 'tp_rate')
    BET_DATE = (By.CLASS_NAME, 'tp_date')
    BET_RESULT = (By.CLASS_NAME, 'tp_result')
    NEXT_BET = (By.ID, 'shadowbox_img_next')
    CLOSE_BET = (By.CLASS_NAME, 'ticket_icon_close')
    SUMMARY = (By.CLASS_NAME, 'summary')
    BOTTOM_INFO = (By.ID, 'bottom-info')