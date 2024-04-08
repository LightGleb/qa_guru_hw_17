import json

import allure
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have, query


def add_product_to_cart_api_post(url, **kwargs):
    with step("API Request"):
        result = requests.post(url="https://demowebshop.tricentis.com" + url, **kwargs)
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True),
                      name="Response", attachment_type=AttachmentType.JSON, extension="json")
    return result


def test_add_notebook_to_cart():
    with step("Add notebook to cart with API"):
        url = "/addproducttocart/catalog/31/1/1"
        result = add_product_to_cart_api_post(url)

        assert result.json()["success"] == True

    with step("Check add notebook to cart with UI"):
        browser.open("https://demowebshop.tricentis.com/cart")
        browser.element('.product-name').should(have.text("14.1-inch Laptop"))


def test_add_cell_phone_to_cart():
    pass
