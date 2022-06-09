from queue import Queue
from bst import BinaryTree, Node
from account import Account
from transaction import TransactionList


# Class implements methods for some transactions
# This class handles amount and fund error handling
class Banker:
    # Uses a global 'accounts' bst instance from the process method to insert account
    def open_account(name, id):
        new_account = Account(name, id)
        if accounts.get(id) == None:
            accounts.put(id, new_account)
            return True
        # Account already exists
        else:
            print('ERROR: Account ' + str(id) + ' is already open. Transaction refused.')

    def deposit(account, amount, fund):
        # Access account through parmeter pass then add to fund
        account.funds[fund] += int(amount)
        return True

    def withdraw(account, amount, fund):
        # Long and Short Bond combo
        if account.funds[fund] < amount:
            if (fund < 4 and (account.funds[2] + account.funds[3] > amount)):
                second_bond = abs(fund - 1)
                amount -= account.funds[fund]
                account.funds[fund] = 0
                account.funds[second_bond] -= amount
                return True
            # Money Market and Prime Market combo
            if (fund < 2 and (account.funds[0] + account.funds[1] > amount)):
                second_market = abs(fund - 1)
                amount -= account.funds[fund]
                account.funds[second_market] = 0
                account.funds[fund] -= amount
                return True

            print('ERROR: Not enough funds to withdraw ' + str(amount) + ' from ' + account.name + ' ' +
                  account.fundnames[fund])
            return False
        else:
            account.funds[fund] -= amount

    def transfer(a, b, fund1, fund2, amount):
        # Money Market and Prime Market combo
        if a.funds[fund1] < amount:
            if (fund1 < 2 and (a.funds[0] + a.funds[1] > amount)):
                second_market = abs(fund1 - 1)
                b.funds[fund2] += amount
                amount -= a.funds[fund1]
                a.funds[fund1] = 0
                a.funds[second_market] -= amount
                return True
            # Long and Short Bond combo
            if (fund1 < 4 and (a.funds[2] + a.funds[3] > amount)):
                second_bond = abs(fund1 - 1)
                b.funds[fund2] += amount
                amount -= a.funds[fund1]
                a.funds[fund1] = 0
                a.funds[second_bond] -= amount
                return True

            print('ERROR: Not enough funds to transfer ' + str(amount) + ' from ' + a.name + ' ' + a.fundnames[fund1])
            return False

        # If amount less than fund process normal transfer
        a.funds[fund1] -= amount
        b.funds[fund2] += amount


# 90% of running code, processes the entire queue
# Error handling in this method is only through account lookup
# Not amount fund comparisons
def process_queue():
    # Create instances of BST,and transaction List to create queue
    global accounts
    accounts = BinaryTree()
    t_list = TransactionList()
    t_list.read_t_file()
    print(t_list.transactions_q.queue)
    while t_list.transactions_q.queue:
        for i in list(t_list.transactions_q.queue):
            # Operation always first item in lists of transaction stored in queue
            operation = i[0]

            # Fund,id,amount parsed through each read of the operation per transaction in the queue
            if operation != 'O':
                id = int(i[1][:-1])
                fund = int(i[1][-1])

            # 'O' calls open function
            if operation == 'O':
                name = str(i[2]) + ' ' + str(i[1])
                id = int(i[3])
                Banker.open_account(name, id)

            # 'D' calls deposit function
            elif operation == 'D':
                fund = int(i[1][-1])
                amount = i[2]
                if accounts.get(id) is None:
                    print('ERROR: Account ' + str(id) + ' not found. Deposit Refused.')
                    accounts.get(id).add_history(fund, i)
                else:
                    # If valid make deposit and add transaction to fund history
                    Banker.deposit(accounts.get(id), amount, fund)
                    result = ' '.join(i)
                    accounts.get(id).add_history(fund, result)
            # 'W' calls withdraw function
            elif operation == 'W':
                amount = int(i[2])
                fund = int(i[1][-1])
                if accounts.get(id) is None:
                    print('ERROR: Account ' + str(id) + ' not found. Withdrawal Refused.')
                    accounts.get(id).add_history(fund, i)
                else:
                    # If valid make withdrawal and add transaction to fund history
                    Banker.withdraw(accounts.get(id), amount, fund)
                    result = ' '.join(i)
                    accounts.get(id).add_history(fund, result)
            # 'T' calls transfer function
            elif operation == 'T':
                amount = int(i[2])
                id2 = int(i[3][:-1])
                fund2 = int(i[3][-1])
                if accounts.get(id) is None:
                    print('ERROR: Account ' + str(id) + ' not found. Transferal Refused.')
                elif accounts.get(id2) is None:
                    print('ERROR: Account ' + str(id2) + ' not found. Transferal Refused.')
                else:
                    # If valid make Transfer and add transaction to fund history for BOTH accounts
                    Banker.transfer(accounts.get(id), accounts.get(id2), fund, fund2, amount)
                    result = ' '.join(i)
                    accounts.get(id).add_history(fund, result)
                    accounts.get(id).add_history(fund2, result)
            # 'H' calls history displays which is in the Account class methods
            elif operation == 'H':
                id = int(i[1][:-1])
                fund = int(i[1][-1])

                if len(i[1]) < 5:
                    id = int(i[1])

                    if accounts.get(id) is None:
                        print('ERROR: Account ' + str(id) + ' not found. Transferal Refused.')
                        return False

                    print('Transaction History for ' + name + ' by fund.')
                    accounts.get(id).display_dict()
                else:
                    print('Transaction History for ' + name + ' ' + str(accounts.get(id).fundnames[fund]) + ': $' + str(
                        accounts.get(id).funds[fund]))
                    accounts.get(id).display_fund_history(fund)

            # Pop each item of the queue at the end
            t_list.transactions_q.queue.popleft()
    # Final display call
    print('\n' + 'Processing Done. Final Balances')
    accounts.display()
