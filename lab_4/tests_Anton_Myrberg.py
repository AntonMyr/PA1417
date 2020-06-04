import pytest
import sqlite3
from fixtures import clean_db, customers, fetch_customers
from selenium import webdriver

import time

frontend_path = "http://127.0.0.1/"

conn = sqlite3.connect("pos.db")
cursor = conn.cursor()


def test_validate_existing_customer(clean_db, customers):
    try:
        driver = webdriver.Firefox()

        driver.get(frontend_path)
        assert driver.title == "Customer Care"

        first_customer_id = customers[0]["ID"]
        first_customer = driver.find_element_by_id(first_customer_id)

        first_customer_fullname = "{} {}".format(
            customers[0]["Firstname"], customers[0]["Lastname"])

        assert first_customer is not None
        assert first_customer.text == first_customer_fullname

        first_customer.click()

        lastname_element = driver.find_element_by_id("lastname")
        assert lastname_element is not None
        assert lastname_element.get_attribute(
            "value") == customers[0]["Lastname"]

        driver.close()
    except Exception as e:
        driver.close()


def test_create_new_customer(clean_db):
    try:
        driver = webdriver.Firefox()

        driver.get(frontend_path)

        driver.find_element_by_xpath(
            "//div[@class='three columns rounded_blue_table']/button").click()

        saveButton = driver.find_element_by_id("save_customer_btn")
        assert saveButton is not None

        inputFieldIds = ["firstname", "lastname", "age", "gender",
                         "nationality", "street", "zipcode", "city", "email"]
        inputKeys = ["Anton", "Myrberg", "20", "male", "Swedish",
                     "Test 1", "17321", "Karlskrona", "anton@myr.com"]

        for i in range(len(inputFieldIds)):
            element = driver.find_element_by_id(inputFieldIds[i])
            element.send_keys(inputKeys[i])

        saveButton.click()
        print("Start : %s" % time.ctime())
        time.sleep(10)
        print("End : %s" % time.ctime())
        all_customers = fetch_customers()
        itemExistsCounter = 0
        for key, val in all_customers[1].items():
            if val in inputKeys:
                itemExistsCounter += 1

        assert itemExistsCounter == 7
        driver.close()
    except Exception as e:
        print(e)
        driver.close()
