import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
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

    # Basket with zero products,
    # An empty basket has a sub-total, discount and total each of zero.
    def test_basket_is_empty(self):
        self.init_basket_pricer = BasketPricer(
            {}, catalogue, offers
        )
        self.assertEquals(
            self.init_basket_pricer.handle(),
            {
                'sub-total': 0,
                'offer': {
                    'Baked-Beans': 'buy 2 get 1 free',
                    'Sardines': '25% discount'
                },
                'total': 0
            }
        )

    # Baskets cannot have a negative price.
    # Still need to implement
    def test_basket_cannot_have_a_negative_price(self):
        self.init_basket_pricer = BasketPricer(
            {}, catalogue, offers
        )
        self.assertEquals(
            self.init_basket_pricer.handle(),
            {
                'sub-total': 0,
                'offer': {
                    'Baked-Beans': 'buy 2 get 1 free',
                    'Sardines': '25% discount'
                },
                'total': 0
            }
        )

    def test_successfull_transaction(self):
        self.init_basket_pricer = BasketPricer(
            basket_1, catalogue, offers
        )
        self.assertEquals(
            self.init_basket_pricer.handle(), 
            {
                'sub-total': 5.16,
                "offer": {
                        "Baked-Beans": "buy 2 get 1 free",
                        "Sardines": "25% discount"
                },
                "total": 5.16
            }
        )

    def test_basket_doesnt_match_catalogue(self):
        self.init_basket_pricer = BasketPricer(
            basket_1_wrong, catalogue, offers
        )
        with self.assertRaises(ValueError):
            self.init_basket_pricer.handle_items()

    def test_basket_does_match_catalogue_but_not_the_offers(self):
        self.init_basket_pricer = BasketPricer(
            basket_1, catalogue, {"fake-offer": "buy 2 get 1 free", }
        )
        with self.assertRaises(ValueError):
            self.init_basket_pricer.apply_offers(basket_1)
