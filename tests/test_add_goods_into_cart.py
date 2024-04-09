import json

import allure
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have

from tests.conftest import get_cookie


def add_product_to_cart_api_post(url, **kwargs):
    with step("API Request"):
        result = requests.post(url="https://demowebshop.tricentis.com" + url, **kwargs)
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True),
                      name="Response", attachment_type=AttachmentType.JSON, extension="json")
    return result


def test_add_notebook_to_cart():
    cookie = get_cookie()

    browser.open('')
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
    browser.open('')

    with step("Add notebook to cart with API"):
        url = "/addproducttocart/catalog/31/1/1"
        result = add_product_to_cart_api_post(url, cookies={'NOPCOMMERCE.AUTH': cookie})

        assert result.json()["success"] is True

    with step("Check add notebook to cart with UI"):
        browser.open("/cart")
        browser.element('.product-name').should(have.text("14.1-inch Laptop"))

    with step("Clear cart with UI"):
        browser.element(".qty-input").clear()
        browser.element(".qty-input").set_value("0").press_enter()


def test_add_cell_phone_to_cart():
    cookie = get_cookie()

    browser.open('')
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
    browser.open('')

    with step("Add notebook to cart with API"):
        url = "/addproducttocart/catalog/43/1/1"
        result = add_product_to_cart_api_post(url, cookies={'NOPCOMMERCE.AUTH': cookie})

        assert result.json()["success"] is True

    with step("Check add notebook to cart with UI"):
        browser.open("/cart")
        browser.element('.product-name').should(have.text("Smartphone"))

    with step("Clear cart with UI"):
        browser.element(".qty-input").clear()
        browser.element(".qty-input").set_value("0").press_enter()
