import os
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from prettytable import PrettyTable

month_year = {0: "Enero",
              1: "Febrero",
              2: "Marzo",
              3: "Abril",
              4: "Mayo",
              5: "Junio",
              6: "Julio",
              7: "Agosto",
              8: "Septiembre",
              9: "Octubre",
              10: "Noviembre",
              11: "Diciembre"}


class Email:
    """
    Class to build email and send it
    """

    def __init__(self, total, monthly_transactions, list_credit_amount, list_debit_amount):
        self.total = total
        self.monthly_transactions = monthly_transactions
        self.list_credit_amount = list_credit_amount
        self.list_debit_amount = list_debit_amount

    def create_table(self):
        tabular_fields = ["Mes", "Número de operaciones"]
        tabular_table = PrettyTable()
        tabular_table.field_names = tabular_fields
        for i in range(len(self.monthly_transactions)):
            if self.monthly_transactions[i]:
                tabular_table.add_row([month_year[i], self.monthly_transactions[i]])
        return tabular_table.get_html_string()

    def create_html(self):
        table = self.create_table()

        data_text = """<br><br>Balance total: {}\
                        <br>Importe promedio de débito: {}\
                        <br>Importe promedio de credito: {}
        """
        avr_debit_amount = sum(self.list_debit_amount) / len(self.list_debit_amount)
        avr_credit_amount = sum(self.list_credit_amount) / len(self.list_credit_amount)
        data_text = data_text.format(self.total, avr_debit_amount, avr_credit_amount)
        html = "<html>" \
               "<head>" \
               "<style>" \
               "table, th, td {" \
               "border: 1px solid black;" \
               "border-collapse: collapse;" \
               "}" \
               "th, td {" \
               "padding: 5px;" \
               "text-align: left;" \
               + "}" \
                 "</style>" \
                 "</head>" \
                 "<body>" \
                 "<p>Este es tu resumen de movimientos, no dudes en contactarnos para cualquier aclaración<br>" \
               + "{}<br>".format(data_text) \
               + "Visitanos: <a href=\"https://www.storicard.com/\">www.storicard.com</a><br>" \
               + "{}".format(table) \
               + "</p>" \
                 "</body>" \
                 "</html>"
        return html

    def send_mail(self):
        html = self.create_html()
        load_dotenv()
        ctx = ssl.create_default_context()
        password = os.getenv("password_google_app")
        sender = os.getenv("sender")
        receiver = os.getenv("receiver")

        message = MIMEMultipart("alternative")
        message["Subject"] = "Hello Multipart World! test pass"
        message["From"] = sender
        message["To"] = receiver

        filename = './images/logo_stori.jpg'
        with open(filename, "rb") as f:
            file = MIMEApplication(f.read())
        disposition = f"attachment; filename={filename}"
        file.add_header("Content-Disposition", disposition)
        message.attach(file)

        message.attach(MIMEText(html, "html"))
        message.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
