# теперь в config.yaml  данные для работы с Selenium есть URL входа:
# далее добавим фикстуру для настройки WebDriver:

import pytest
import requests
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='session')
def config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

@pytest.fixture(scope='session')
def auth_token(config):
    login_url = f"{config['site_url']}/gateway/login"
    response = requests.post(login_url, data={
        "username": config['username'],
        "password": config['password']
    })
    response.raise_for_status()
    return response.json()['token']

@pytest.fixture(scope='session')
def browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()

