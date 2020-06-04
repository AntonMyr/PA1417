import sqlite3
from datachecker import DataChecker
from unittest.mock import Mock, patch

conn = sqlite3.connect("pos.db")
cursor = conn.cursor()


def test_check_valid_age_valid_inputs():
    dc = DataChecker()
    # Test valid age
    assert dc.check_valid_age(5) == True


def test_check_valid_age_invalid_inputs():
    dc = DataChecker()
    # Test letter
    assert dc.check_valid_age("a") == False
    # Test letter
    assert dc.check_valid_age(-1) == False


def test_check_valid_text_field_valid_input():
    dc = DataChecker()
    print("___test_check_valid_text_field___\n")
    # Test valid input
    print("Test valid input...\n")
    assert dc.check_valid_text_field("Hola") == True
    # Test empty string with emptyTextAllowed set to false
    print("Test empty string with emptyTextAllowed set to false...\n")
    assert dc.check_valid_text_field("", False) == True


def test_check_valid_text_field_invalid_input():
    dc = DataChecker()
    # Test empty string with emptyTextNotAllowed set to true
    print("Test empty string with emptyTextNotAllowed set to true...\n")
    assert dc.check_valid_text_field("") == False


def test_customer_has_equipment_attached():

    testCustomerId = 1
    testCustomerNoIMEIPtrId = 2
    with patch("datachecker.sqlite3") as mocksql:
        mocksql.connect().cursor().fetchall.return_value = [
            (
                testCustomerId,
                "Anton",
                "Myrberg",
                20,
                "male",
                "Streetlife",
                195,
                "Stockholm",
                "",
                "",
                1,
                "",
                "",
                "",
            ),
            (
                testCustomerNoIMEIPtrId,
                "Anton",
                "Myrberg",
                20,
                "male",
                "Streetlife",
                195,
                "Stockholm",
                "",
                "",
                "",
                "",
                "",
                "",
            ),
        ]
        mocksql.connect().cursor().fetchone.return_value = [
            (380, "IMEI_0123456789", 1010)
        ]
    dc = DataChecker()

    # ID that can't be found
    assert dc.customer_has_equipment_attached(3) == False

    # Customer exists but equipment id can't be found
    assert dc.customer_has_equipment_attached(testCustomerId) == False

    # Customer exists but has no IMEIPTR
    assert dc.customer_has_equipment_attached(testCustomerNoIMEIPtrId) == False
