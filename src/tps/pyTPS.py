class pyTPS:
    def __init__(self):
        self.transactions = []
        self.numTransactions = 0
        self.mostRecentTransaction = -1
        self.performingDo = False
        self.performingUndo = False

    def isPerformingDo(self):
        return self.performingDo

    def isPerformingUndo(self):
        return self.performingUndo

    def hasTransactionToRedo(self):
        return (self.mostRecentTransaction + 1) < self.numTransactions

    def hasTransactionToUndo(self):
        return self.mostRecentTransaction >= 0

    def addTransaction(self, transaction):
        # ARE WE BRANCHING?
        if (
            self.mostRecentTransaction < 0
            or self.mostRecentTransaction < (len(self.transactions) - 1)
        ):
            for i in range(len(self.transactions) - 1, self.mostRecentTransaction, -1):
                del self.transactions[i]
            self.numTransactions = self.mostRecentTransaction + 2
        else:
            self.numTransactions += 1

        # ADD THE TRANSACTION
        self.transactions.append(transaction)

        # AND EXECUTE IT
        self.doTransaction()

    def doTransaction(self):
        if self.hasTransactionToRedo():
            self.performingDo = True
            transaction = self.transactions[self.mostRecentTransaction + 1]
            transaction.doTransaction()
            self.mostRecentTransaction += 1
            self.performingDo = False

    def undoTransaction(self):
        if self.hasTransactionToUndo():
            self.performingUndo = True
            transaction = self.transactions[self.mostRecentTransaction]
            transaction.undoTransaction()
            self.mostRecentTransaction -= 1
            self.performingUndo = False

    def clearAllTransactions(self):
        self.transactions = []
        self.mostRecentTransaction = -1
        self.numTransactions = 0

    def getSize(self):
        return len(self.transactions)

    def getRedoSize(self):
        return self.getSize() - self.mostRecentTransaction - 1

    def getUndoSize(self):
        return self.mostRecentTransaction + 1

    def toString(self):
        text = "--Number of Transactions: {}\n".format(self.numTransactions)
        text += "--Current Index on Stack: {}\n".format(self.mostRecentTransaction)
        text += "--Current Transaction Stack:\n"
        for i in range(self.mostRecentTransaction + 1):
            transaction = self.transactions[i]
            text += "----{}\n".format(transaction.toString())
        return text
    
    def getTransactions(self):
        return self.transactions


from abc import ABC

class pyTPS_Transaction(ABC):
    def doTransaction(self):
        pass
    
    def undoTransaction(self):
        pass
    
    def redo(self):
        pass
    
    def toString(self):
        pass
