class Bank:  # Define a class named Bank
    def __init__(self, bankId, bankName, bankIFSCode, custId, custName, custAmt, acctType, transDate, transId, transStatus):
        # Initialize the Bank class with the given parameters
        self.bankId = bankId  # Bank ID
        self.bankName = bankName  # Bank name
        self.bankIFSCode = bankIFSCode  # Bank IFSC code
        self.custId = custId  # Customer ID
        self.custName = custName  # Customer name
        self.custAmt = custAmt  # Customer amount
        self.acctType = acctType  # Account type
        self.transDate = transDate  # Transaction date
        self.transId = transId  # Transaction ID
        self.transStatus = transStatus  # Transaction statu