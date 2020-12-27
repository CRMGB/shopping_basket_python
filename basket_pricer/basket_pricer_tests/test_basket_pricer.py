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

basket_wrong_items = {
    "Pinto-Beans": 4,
    "Cookies":  1,
    "Shampoo(Large)": 9
}

basket_negative = {
    "Baked-Beans": -4,
    "Biscuits":  1,
    "Shampoo(Small)": -8   
}

basket_3 = {
    "Sardines": 2,
    "Shampoo(Small)": 5,
    "Shampoo(Medium)": 7
}

class BasketPricerTest(unittest.TestCase):

    def test_basket_is_empty(self):
        self.init_basket_pricer = BasketPricer(
            {}, catalogue, offers
        )
        self.assertEqual(
            self.init_basket_pricer.handle(),
            {
                'sub-total': '£0',
                'offer': {
                    'Baked-Beans': 'buy 2 get 1 free',
                    'Sardines': '25% discount'
                },
                'total': '£0'
            }
        )

    def test_basket_cannot_have_a_negative_price(self):
        self.init_basket_pricer = BasketPricer(
            basket_negative, catalogue, offers
        )
        with self.assertRaises(ValueError):
            self.init_basket_pricer.handle_items()

    def test_successfull_transaction(self):
        self.init_basket_pricer = BasketPricer(
            basket_1, catalogue, offers
        )
        self.assertEqual(
            self.init_basket_pricer.handle(), 
            {
                'sub-total': '£5.16',
                "offer": {
                    "Baked-Beans": "buy 2 get 1 free",
                    "Sardines": "25% discount"
                },
                "total": '£4.17'
            }
        )

    def test_three_for_the_price_of_two(self):
        self.init_basket_pricer = BasketPricer(
            {"Baked-Beans": 3 },catalogue,  {"Baked-Beans": "buy 2 get 1 free"}
        )

        self.assertEqual(
            self.init_basket_pricer.handle(), 
            {
                'sub-total': '£2.97',
                "offer": {"Baked-Beans": "buy 2 get 1 free"},
                "total": '£1.98'
            }
        )
    
    def test_six_for_the_price_of_four(self):
        self.init_basket_pricer = BasketPricer(
            {"Baked-Beans": 6 },catalogue,  {"Baked-Beans": "buy 2 get 1 free"}
        )

        self.assertEqual(
            self.init_basket_pricer.handle(), 
            {
                'sub-total': '£5.94',
                "offer": {"Baked-Beans": "buy 2 get 1 free"},
                "total": '£3.96'
            }
        )

    def test_nine_for_the_price_of_six(self):
        self.init_basket_pricer = BasketPricer(
            {"Baked-Beans": 9 },catalogue,  {"Baked-Beans": "buy 2 get 1 free"}
        )

        self.assertEqual(
            self.init_basket_pricer.handle(), 
            {
                'sub-total': '£8.91',
                "offer": {"Baked-Beans": "buy 2 get 1 free"},
                "total": '£5.94'
            }
        )

    def test_basket_doesnt_match_catalogue(self):
        self.init_basket_pricer = BasketPricer(
            basket_wrong_items, catalogue, offers
        )
        with self.assertRaises(ValueError):
            self.init_basket_pricer.handle_items()

