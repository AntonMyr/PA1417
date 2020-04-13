import sqlite3
from datachecker import DataChecker


dc = DataChecker()
conn = sqlite3.connect("pos.db")
cursor = conn.cursor()


def test_check_valid_age():
    # Test valid age
    assert dc.check_valid_age(5) == True
    # Test letter
    assert dc.check_valid_age("a") == False
    # Test letter
    assert dc.check_valid_age(-1) == False


def test_check_valid_text_field():
    print("___test_check_valid_text_field___\n")
    # Test valid input
    print("Test valid input...\n")
    assert dc.check_valid_text_field("Hola") == True
    # Test empty string with emptyTextNotAllowed set to true
    print("Test empty string with emptyTextNotAllowed set to true...\n")
    assert dc.check_valid_text_field("") == False
    # Test empty string with emptyTextAllowed set to false
    print("Test empty string with emptyTextAllowed set to false...\n")
    assert dc.check_valid_text_field("", False) == True


def test_customer_has_equipment_attached():
    # Problems with "can't write readonly database"
    cursor.execute(
        """INSERT INTO Customers (Firstname, Lastname, Age, Sex, Street, Zip, City, IMEIPtr) VALUES ('Anton', 'Myrberg', 20, 'male', 'Streetlife', 195, 'Stockholm', 1); """
    )
    conn.commit()
    testCustomerId = cursor.lastrowid

    cursor.execute(
        """INSERT INTO Customers (Firstname, Lastname, Age, Sex, Street, Zip, City) VALUES ('Anton', 'Myrberg', 20, 'male', 'Streetlife', 195, 'Stockholm'); """
    )
    conn.commit()
    testCustomerNoIMEIPtrId = cursor.lastrowid

    assert dc.customer_has_equipment_attached(1) == False

    # Customer exists but equipment id can't be found
    assert dc.customer_has_equipment_attached(testCustomerId) == False
    # assert dc.customer_has_equipment_attached(514) == False

    # Customer exists but has no IMEIPTR
    assert dc.customer_has_equipment_attached(testCustomerNoIMEIPtrId) == False
    # assert dc.customer_has_equipment_attached(515) == False

    cursor.execute(
        """DELETE FROM Customers WHERE ID = ?;""", (testCustomerId,),
    )
    conn.commit()

    cursor.execute(
        """DELETE FROM Customers WHERE ID = ?;""", (testCustomerNoIMEIPtrId,),
    )
    conn.commit()
