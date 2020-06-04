import pytest
import requests
import shutil

database_path = "/home/pft/restapi/point-of-sale/pos.db"
database_backup_path = "/home/pft/restapi/point-of-sale/pos_bak.db"
rest_api_url = "http://127.0.0.1:6399"


@pytest.fixture()
def clean_db():
    shutil.copy(database_backup_path, database_path)


def fetch_customers():
    result = requests.get(rest_api_url + "/customers")
    if result.status_code == 200:
        customers = result.json()
    else:
        raise Exception(
            f"Couldn't retrieve customers via REST API. \nStatus code: {result.status_code}")
    return customers


@pytest.fixture()
def customers():
    customers = fetch_customers()
    return customers
