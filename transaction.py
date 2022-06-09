from queue import Queue

#TransactionList queue object
class TransactionList:
    def __init__(self):
        self.transactions_q = Queue()
    
    def read_t_file (self):
        #Reads file specified and takes each line and indices of each line into a list
        with open('BankTransIn.txt') as f:
            lines = [line.split() for line in f]
        for trans in lines:
            self.transactions_q.put(trans)



    
        
        


