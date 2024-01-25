import json
from datetime import datetime

class Transaction:
    '''
    Инициализирует объект транзакции на основе переданных данных.

    Parameters:
    - data (dict): Словарь с данными транзакции.

    Attributes:
    - id (str): Идентификатор транзакции.
    - state (str): Состояние транзакции.
    - date (str): Дата транзакции в формате "день.месяц.год".
    - amount (str): Сумма транзакции.
    - currency (str): Валюта транзакции.
    - description (str): Описание транзакции.
    - from_account (str): Исходный счет/карта транзакции.
    - to_account (str): Целевой счет/карта транзакции.
    '''
    def __init__(self, data):
        self.id = str(data.get("id", ""))
        self.state = str(data.get("state", ""))
        self.date = self.parse_date(data.get("date", ""))
        self.amount = str(data.get("operationAmount", {}).get("amount", ""))
        self.currency = str(data.get("operationAmount", {}).get("currency", {}).get("name", ""))
        self.description = str(data.get("description", ""))
        self.from_account = str(data.get("from", ""))
        self.to_account = str(data.get("to", ""))

    def display(self):
        '''
        Выводит на экран отформатированную информацию о транзакции.

        Formatted Output:
        - Дата и описание транзакции.
        - Отмаскированный номер исходного счета/карты -> Отмаскированный номер целевого счета/карты.
        - Сумма транзакции и валюта.
        '''
        masked_from_account = self.mask_account_number(self.from_account)
        masked_to_account = self.mask_account_number(self.to_account)

        print(f"{self.date} {self.description}")
        print(f"{masked_from_account} -> {masked_to_account}")
        print(f"{self.amount} {self.currency}")
        print()

    @staticmethod
    def mask_account_number(account_number):
        '''
        Маскирует номер счета/карты в соответствии с заданным форматом.

        Parameters:
        - account_number (str): Номер счета/карты.

        Returns:
        - str: Отмаскированный номер счета/карты.
        '''
        if account_number.startswith("Visa"):
            # Маскировка номера карты для карт Visa
            card_number_parts = account_number.split(' ')
            return (f"{card_number_parts[0]} {card_number_parts[1][:4]} {card_number_parts[1][4:8]}"
                    f" {card_number_parts[2][:4]} {card_number_parts[2][4:6]}** **** {card_number_parts[2][-4:]}")
        elif account_number.startswith("MasterCard") or account_number.startswith("Maestro") or account_number.startswith("МИР"):
            # Маскировка номера карты для карт Maestro, MasterCard, МИР
            card_number_parts = account_number.split(' ')
            return (
                f"{card_number_parts[0]} {card_number_parts[1][:4]} {card_number_parts[1][4:6]}** **** {card_number_parts[1][-4:]}")
        elif account_number.startswith("Счет"):
            # Маскировка номера счета
            return f"**{account_number.split(' ')[-1][-4:]}"
        else:
            # В случае других типов счетов (просто для примера, можно дополнить)
            return account_number

    @staticmethod
    def parse_date(date_str):
        '''
        Преобразует строку с датой в формате ISO в строку с датой в формате "день.месяц.год".

        Parameters:
        - date_str (str): Строка с датой в формате ISO.

        Returns:
        - str: Строка с датой в формате "день.месяц.год".
        '''
        try:
            return datetime.fromisoformat(date_str).strftime('%d.%m.%Y')
        except (ValueError, TypeError):
            return ""

# Чтение данных из файла JSON с кодировкой utf-8
with open('operations.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Создание объектов Transaction для каждой транзакции
transactions = [Transaction(entry) for entry in data]

# Сортировка транзакций по дате в обратном порядке
sorted_transactions = sorted(transactions, key=lambda x: x.date, reverse=True)

# Вывод последних 5 выполненных операций
for transaction in sorted_transactions[:5]:
    transaction.display()
