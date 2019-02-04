from core.utility import printf
from pandas.io.json import json_normalize

TAX = 0.88


class User:
    def __init__(self, history, deposits, only_resolved):
        self.history = json_normalize(history)
        self.deposits = json_normalize(deposits)
        self.all_events = json_normalize(history, record_path='events')
        if only_resolved: self.remove_pending_bets()
        self.total = self.calculate_totals()
        self.indexes = self.calculate_indexes()

    def remove_pending_bets(self):
        self.history = self.history[self.history.status != 'P']
        self.all_events = self.all_events[self.all_events.win != 'P']

    def calculate_totals(self):
        return {
            'deposit': self.deposits['value'].sum(),
            'stake': self.history['stake'].sum(),
            'potential_payout': self.history['potential_payout'].sum(),
            'payout': self.history['payout'].sum(),
            'profit': self.history['payout'].sum() - self.history['stake'].sum()
        }

    def calculate_indexes(self):
        return {
            'roi': self.roi(),
            'streak_singles': self.streak(),
            'streak_acco': self.streak_acco()
        }

    # ANALYSIS

    def roi(self):
        return ((self.total['payout'] - self.total['stake'])/self.total['stake'])*100

    def bet_with_constant_stake_no_acco(self, stake, tax):
        # something is wrong with this function
        events = self.all_events
        num_of_total_bets = len(events)
        won_bets = events[events.win == 'Y']
        num_of_won_bets = len(won_bets)
        won_odds = list(won_bets['odds'])
        if tax:
            total_winnings = sum([(x*stake*TAX)-stake for x in won_odds])  # should be profit or no?
        else:
            total_winnings = sum([(x*stake)-stake for x in won_odds])  # should be profit or no?
        total_loss = (num_of_total_bets - num_of_won_bets) * stake
        return total_winnings-total_loss

    def streak(self):
        table = self.all_events
        res = dict(table['win'].value_counts())
        y, n = res['Y'], res['N']
        return y / (y+n) * 100

    def streak_acco(self):
        table = self.history
        win = table['status'] == 'W'
        res = dict(win.value_counts())
        y = res[True] if True in res else 0
        n = res[False] if False in res else 0
        return y / (y+n) * 100

    def show_data(self):
        for key, val in self.total.items():
            header = [word.upper() for word in key.split('_')]
            header = 'TOTAL ' + ' '.join(header) + ': '
            printf(header, val, 'cash')

        print()

        for key, val in self.indexes.items():
            header = [word.upper() for word in key.split('_')]
            header = ' '.join(header) + ': '
            printf(header, val, 'percent')





