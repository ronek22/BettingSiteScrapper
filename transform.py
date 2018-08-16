import json
from pandas.io.json import json_normalize

TAX = 0.88

with open('bettingHistory.json', 'r') as f:
    data = json.load(f)


def roi(total_stake, total_payout):
    # it doing it wrong
    result = ((total_payout - total_stake)/total_stake)*100
    return cash_format(result) + "%"


def streak(table):
    res = dict(table['win'].value_counts())
    y, n = res['Y'], res['N']
    return cash_format(y / (y+n)*100) + "%"


def streak_acco(table):
    win = table['payout'] > 0
    res = dict(win.value_counts())
    y, n = res[True], res[False]
    return cash_format(y / (y+n)*100) + "%"


def cash_format(cash):
    return "{0:.2f}".format(cash)


def bet_with_constant_stake_no_acco(events, stake):
    # something is wrong with this function
    num_of_total_bets = len(events)
    won_bets = events[events.win == 'Y']
    num_of_won_bets = len(won_bets)
    won_odds = list(won_bets['odds'])
    total_winnings = sum([(x*stake*TAX)-stake for x in won_odds])  # should be profit or no?
    total_loss = (num_of_total_bets - num_of_won_bets) * stake
    return cash_format(total_winnings-total_loss)


def possibility_of_no_acco_strategy(events, investment, parts, tax):
    balance = investment
    stake = balance / parts
    subset = events[['odds', 'win']]
    bets = [tuple(x) for x in subset.values]

    for bet in bets:
        balance -= stake
        if bet[1] == 'Y':
            profit = stake*bet[0]*TAX if tax else stake*bet[0]
            balance += profit
        if balance < 0:
            return False
    return "\nIT POSSIBLE, YOU'VE INVESTED {} $, YOU'VE EVERY BET HAS STAKE {} $, NOW YOU CAN WITHDRAWAL {} $".format(investment, stake, cash_format(balance)) 


def run_analysis():
    table = json_normalize(data)
    all_events = json_normalize(data, record_path='events')

    total_stake = table['stake'].sum()
    total_pot_payout = table['potential_payout'].sum()
    total_payout = table['payout'].sum()
    print("TOTAL STAKE: ", cash_format(total_stake))
    print("TOTAL POTENTIAL PAYOUT: ", cash_format(total_pot_payout))
    print("TOTAL PAYOUT: ", cash_format(total_payout), '\t|\tROI: ' + roi(total_stake, total_payout))
    print("PROFIT: ", cash_format(total_payout - total_stake))
    print("\nSTREAK WITHOUT ACCUMULATOR", streak(all_events))
    print("STREAK WITH ACCUMULATOR", streak_acco(table))
    print("\nSINGLE BETS WITH CONSTANT STAKE CAN PRODUCE GIVEN PROFIT: "  + bet_with_constant_stake_no_acco(all_events, 10))
    print("POSSIBILITY OF NO ACCO STRATEGY WITH TAXES", possibility_of_no_acco_strategy(all_events, 1000, 100, True))
    print("POSSIBILITY OF NO ACCO STRATEGY WITHOUT TAXES", possibility_of_no_acco_strategy(all_events, 1000, 100, False))
