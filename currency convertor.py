import requests
import tkinter as tk
from tkinter import ttk
import re

class RealTimeCurrencyConverter:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]  # converting into USD as our base currency is USD
        amount = round(amount * self.currencies[to_currency], 4)
        return amount

url = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(url)
print(converter.convert('INR', 'SGD', 1000))

class App(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.title('Currency Converter')
        self.currency_converter = converter

        # Size
        self.geometry("803x522")
        self.configure(bg='white')

        # Label
        self.intro_label = tk.Label(self, text="Real Time Currency Converter", bg='#63C6FE',fg='white', relief=tk.RAISED, borderwidth=2)
        self.intro_label.config(font=('Inter', 40, 'bold'))

        # Date
        self.date_label = tk.Label(self, text=f"Date: {self.currency_converter.data['date']}",bg='white',fg='black')
        self.date_label.config(font=('Inter', 40, 'bold'))

        self.intro_label.place(x=65, y=28,width=803,height=107)
        self.date_label.place(x=237, y=136)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.entry_field = tk.Entry(self, bd=5, relief=tk.RIDGE, justify=tk.CENTER, validate='key',width=20, validatecommand=valid)
        self.result_field_label = tk.Label(self, text='', fg='black', bg='#D9D9D9', relief=tk.RIDGE, justify=tk.CENTER, width=20, borderwidth=3)

        # Currency Dropdown
        self.from_currency_variable = tk.StringVar(self)
        self.from_currency_variable.set("INR")  # default value
        self.to_currency_variable = tk.StringVar(self)
        self.to_currency_variable.set("USD")  # default value

        font = ("Inter", 32, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable, values=list(self.currency_converter.currencies.keys()), font=font, state='readonly', width=12, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable, values=list(self.currency_converter.currencies.keys()), font=font, state='readonly', width=12, justify=tk.CENTER)

        self.from_currency_dropdown.place(x=87, y=215)
        self.entry_field.place(x=106, y=324, height=59)
        self.to_currency_dropdown.place(x=507, y=215)
        self.result_field_label.place(x=526, y=324, height=59)

        # Convert Button
        self.convert_button = tk.Button(self, text='Convert', fg='black', width=20, command=self.perform)
        self.convert_button.config(font=('Inter', 32, 'bold'))
        self.convert_button.place(x=276, y=440,width=250,height=55)

    def perform(self):
        amount = float(self.entry_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        self.result_field_label.config(text=str(converted_amount))

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"^[0-9]*\.?[0-9]*$")
        result = regex.match(string)
        return string == "" or (string.count('.') <= 1 and result is not None)

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)

    app = App(converter)
    app.mainloop()
