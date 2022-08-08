from processes import CalculateTransactions
from send_email_app import Email

calculate_transacions = CalculateTransactions("transactions.csv")
total, monthly_transactions, list_credit_amount, list_debit_amount = calculate_transacions.calculator()

class_email = Email(total=total,
                    monthly_transactions=monthly_transactions,
                    list_credit_amount=list_credit_amount,
                    list_debit_amount=list_debit_amount)
class_email.send_mail()
