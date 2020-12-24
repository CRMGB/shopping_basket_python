import unittest

from basket_pricer import BasketPricer

# Change this to a model
catalogue = {
    "Baked-Beans": 0.99,
    "Biscuits": 1.20,
    "Sardines": 1.89,
    "Shampoo(Small)": 2.00,
    "Shampoo(Medium)": 2.50,
    "Shampoo(Large)": 3.50
}

offers = {
    "Baked-Beans": "buy 2 get 1 free",
    "Sardines": "25% discount"
}

basket_1 = {
    "Baked-Beans": 4,
    "Biscuits":  1
}

basket_1_wrong = {
    "Pinto-Beans": 4,
    "Cookies":  1
}

basket_2 = {
    "Baked-Beans": 2,
    "Biscuits":  1,
    "Sardines": 2
}


class BasketPricerTest(unittest.TestCase):

    def test_basket_doesnt_match_catalogue(self):
        self.init_basket_pricer = BasketPricer(
            basket_1_wrong, catalogue, offers
        )
        with self.assertRaises(ValueError):
            self.init_basket_pricer.get_basket_and_catalogue()

    def test_basket_does_match_catalogue_but_not_the_offers(self):
        self.init_basket_pricer = BasketPricer(
            basket_1, catalogue, offers
        )
        self.init_basket_pricer.get_basket_and_catalogue()
