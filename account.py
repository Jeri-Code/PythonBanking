# Class Account Object holds all information on a given account
class Account:
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.funds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.fundnames = ['Money Market', 'Prime Money Market', 'Long-Term Bond', 'Short-Term Bond', \
                          '500 Index Fund', 'Capital Value Fund', 'Growth Equity Fund', \
                          'Growth Index Fund', 'Value Fund', 'Value Stock Index']
        # History of each fund accessed through a dictionary of lists
        self.history = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

    '''Series of methods handling the displaying and interactions with history'''

    # Appends to list of the respective fund keyt
    def add_history(self, fund, history):
        self.history[fund].append(history)

    # Displays all balances of each fund
    def display_balance(self):
        print(self.name + ' Account ID: ' + str(self.id))
        for i in range(10):
            print(' ' + (self.fundnames[i]) + ': $' + str(self.funds[i]) + '\n')
        print('\n')
        return

    # Formats and prints values of each fund key history val
    def display_fund_history(self, fund):
        print(', '.join(self.history[fund]))

    # Show all history for each fund
    def display_dict(self):
        for key, value in self.history.items():
            if self.funds[key] > 0:
                print(' ' + (self.fundnames[key]) + ': $' + str(self.funds[key]) + '\n')
                string = "\n".join([str(item) for item in value])
                print(str(string) + '\n')
