# Code by Anton Myrberg 2020-04-24
import requests
import shutil
import pprint

# Debugging purposes
pp = pprint.PrettyPrinter(indent=4)


def test_get_customers():
    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos_bak.db",
        "/home/pft/restapi/point-of-sale/pos.db",
    )
    response = requests.get("http://localhost:6399/customers")
    customers = response.json()
    assert len(customers) == 1


def test_create_customer():
    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos_bak.db",
        "/home/pft/restapi/point-of-sale/pos.db",
    )
    payload = {
        "Firstname": "Anton",
        "Lastname": "Myrberg",
        "Age": "30",
        "Sex": "Male",
        "Street": "Lookitup 20",
        "Zip": "371",
        "City": "Karlskrona",
        "Nationality": "Swedish",
        "Email": "anton@anton.com",
        "Password": "anton",
    }
    response = requests.post("http://localhost:6399/customers", json=payload)
    assert response.status_code == 201
    createdCustomer = response.json()
    assert createdCustomer["ID"] == 514

    samePairs = 0
    for key, value in payload.items():
        if createdCustomer[key] == payload[key]:
            samePairs += 1
    # samePairs is only 9 because the API adds 1 to Age and also makes it into an integer
    assert samePairs == 9
    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos.db",
        "/home/pft/restapi/point-of-sale/pos_created_customer.db",
    )


def test_create_sims():
    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos_created_customer.db",
        "/home/pft/restapi/point-of-sale/pos.db",
    )

    payload = {"IMSI": "IMSI_0123456789", "MSISDN": "+46723580953"}
    response = requests.post("http://localhost:6399/sims", json=payload)
    createdSim = response.json()
    assert response.status_code == 201
    samePairs = 0
    for key, value in payload.items():
        if createdSim[key] == payload[key]:
            samePairs += 1

    assert samePairs == 2

    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos.db",
        "/home/pft/restapi/point-of-sale/pos_created_customer_and_sim.db",
    )


def test_update_customer_IMSIPtr():
    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos_created_customer_and_sim.db",
        "/home/pft/restapi/point-of-sale/pos.db",
    )
    payload = {
        "Firstname": "Anton",
        "Lastname": "Myrberg",
        "Age": "21",
        "Sex": "Male",
        "Street": "Lookitup 20",
        "Zip": "371",
        "City": "Karlskrona",
        "Nationality": "Swedish",
        "IMSIPtr": "636",
        "Email": "anton@myrberg.com",
        "Password": "anton",
    }

    requests.put("http://localhost:6399/customers/514", json=payload)
    response = requests.get("http://localhost:6399/customers/514")
    updatedCustomer = response.json()

    samePairs = 0
    for key, value in payload.items():
        if updatedCustomer[key] == payload[key]:
            samePairs += 1

    assert samePairs == 8


def test_create_product():
    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos_created_customer.db",
        "/home/pft/restapi/point-of-sale/pos.db",
    )

    payload = {"IMEI": "IMEI_336699", "ProductPtr": 1010}

    response = requests.post("http://localhost:6399/equipments", json=payload)
    createdProduct = response.json()
    samePairs = 0
    for key, value in payload.items():
        if createdProduct[key] == payload[key]:
            samePairs += 1
    assert samePairs == 2

    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos.db",
        "/home/pft/restapi/point-of-sale/pos_created_customer_and_equipment.db",
    )


def test_update_customer_IMEIPtr():
    shutil.copy(
        "/home/pft/restapi/point-of-sale/pos_created_customer_and_equipment.db",
        "/home/pft/restapi/point-of-sale/pos.db",
    )

    payload = {
        "Firstname": "Anton",
        "Lastname": "Myrberg",
        "Age": "21",
        "Sex": "Male",
        "Street": "Lookitup 20",
        "Zip": "371",
        "City": "Karlskrona",
        "Nationality": "Swedish",
        "IMEIPtr": "381",
        "Email": "anton@myrberg.com",
        "Password": "anton",
    }

    response = requests.get("http://localhost:6399/equipments")

    requests.put("http://localhost:6399/customers/514", json=payload)
    response = requests.get("http://localhost:6399/customers/514")
    updatedCustomer = response.json()

    assert updatedCustomer["IMEIPtr"] == 381

    samePairs = 0
    for key, value in payload.items():
        if updatedCustomer[key] == payload[key]:
            samePairs += 1

    assert samePairs == 8
