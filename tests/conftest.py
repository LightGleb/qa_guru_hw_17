import allure
import pytest
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have

LOGIN = "glebov@gmail.com"
PASSWORD = "123456"
URL = "https://demowebshop.tricentis.com/"


@pytest.fixture(scope='function', autouse=True)
def login():
    with step("Login with API"):
        result = requests.post(
            url=URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
    with step("Get cookie from API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with step("Set cookie from API"):
        browser.open(URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(URL)

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))

    yield

    browser.quit()
