import json
from datetime import datetime
from funcs.operations import Transaction


def test_mask_account_number():
    assert Transaction.mask_account_number("Visa Platinum 1234567890123456") == "Visa Platinum 1234 56** **** 3456"
    assert Transaction.mask_account_number("MasterCard 9876543210987654") == "MasterCard 9876 54** **** 7654"


def test_parse_date():
    assert Transaction.parse_date("2022-01-30T12:30:45.678901") == "30.01.2022"


def test_display(capsys):
    data = {
        "id": 123,
        "state": "EXECUTED",
        "date": "2022-01-30T12:30:45.678901",
        "operationAmount": {"amount": 100, "currency": {"name": "USD"}},
        "description": "Test Transaction",
        "from": "Visa Platinum 1234 5678 9012 3456",
        "to": "Счет 9876543210"
    }
    transaction = Transaction(data)
    transaction.display()

    captured = capsys.readouterr()
    assert "30.01.2022 Test Transaction" in captured.out
