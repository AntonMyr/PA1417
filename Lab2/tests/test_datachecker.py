from datachecker import DataChecker


dc = DataChecker()


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


# def test_customer_has_equipment_attached():
