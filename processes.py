from datetime import datetime
from typing import List, Tuple

from utils.database import read_table


class CalculateTransactions:
    """
    Class to calculate the client transactions
    file_transactions is a csv file with this format:
    ID,DATE,TRANSACTION
    1,01/01/22,290.41
    2,02/01/22,-65.02
    """
    def __init__(self, file_transactions: str):
        self.file_transactions = file_transactions

    def read_table(self) -> Tuple[List[datetime], List[float]]:
        dates_transactions = list()
        amounts_transactions = list()
        database_records = read_table("transactions")
        for row in database_records:
            dates_transactions.append(datetime.strptime(row[1][:10], "%Y-%m-%d"))
            amounts_transactions.append(row[2])
        return dates_transactions, amounts_transactions

    def calculator(self) -> Tuple[float, List[int], List[float], List[float]]:
        dates_transactions, amounts_transactions = self.read_table()
        total = 0
        monthly_transactions = [int(0) for _ in range(12)]
        list_credit_amount = list()
        list_debit_amount = list()
        transactions = len(dates_transactions)
        for i in range(transactions):
            month = dates_transactions[i].month - 1
            monthly_transactions[month] += int(1)
            total += amounts_transactions[i]
            if amounts_transactions[i] >= 0:
                list_credit_amount.append(amounts_transactions[i])
            else:
                list_debit_amount.append(amounts_transactions[i])
        return total, monthly_transactions, list_credit_amount, list_debit_amount


"""
calculate_transacions = CalculateTransactions("transactions.csv")
print(calculate_transacions.calculator())
"""
