import unittest
from basket_pricer import BasketPricer

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

my_offer = {
    "Baked-Beans": "buy 2 get 1 free",
    "Shampoo(Small)": "17% discount",
    "Biscuits": "buy 2 get 1 free"
}

new_offer = {
    "Shampoo(Small)": "Buy 3, get the cheapest one for free",
    "Shampoo(Medium)": "Buy 3, get the cheapest one for free",
    "Shampoo(Large)": "Buy 3, get the cheapest one for free"
}

my_new_offer = {
    "Biscuits": "Buy 5, get the cheapest one for free",
}

basket_1 = {
    "Baked-Beans": 4,
    "Biscuits":  1
}

basket_2 = {
    "Baked-Beans": 2,
    "Biscuits":  1,
    "Sardines": 2
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
    "Shampoo(Small)": 1,
    "Biscuits": 7,
    "Baked-Beans": 11
}

basket_4 = {
    "Shampoo(Large)": 3,
    "Shampoo(Medium)": 1,
    "Shampoo(Small)": 2
}

class BasketPricerTest(unittest.TestCase):

    def setUp(self):
        self.init_basket_pricer = BasketPricer(
            basket_1, catalogue, offers
        )

    def test_basket_is_empty(self):

        self.assertEqual(
            self.init_basket_pricer.handle({}),
            {
                'sub-total': '£0',
                'discount': '£0',
                'total': '£0'
            }
        )

    def test_basket_cannot_have_a_negative_price(self):
        with self.assertRaises(Exception):
            self.init_basket_pricer.handle_items(basket_negative)

    def test_successfull_transaction_1(self):
        self.assertEqual(
            self.init_basket_pricer.handle(basket_1),
            {
                'sub-total': '£5.16',
                'discount': '£0.99',
                "total": '£4.17'
            }
        )

    def test_successfull_transaction_2(self):
        self.assertEqual(
            self.init_basket_pricer.handle(basket_2),
            {
                'sub-total': '£6.96',
                'discount': "£0.95",
                "total": '£6.01'
            }
        )

    def test_my_successfull_transaction(self):
        self.init_basket_pricer = BasketPricer(
            basket_3, catalogue, my_offer
        )
        self.assertEqual(
            self.init_basket_pricer.handle(basket_3),
            {
                'sub-total': '£25.07',
                'discount': '£0.34',
                "total": '£24.73'
            }
        )

    def test_my_successfull_transaction_2(self):
        self.init_basket_pricer = BasketPricer(
            basket_3, catalogue, {"Baked-Beans": "buy 4 get 2 free"}
        )
        self.assertEqual(
            self.init_basket_pricer.handle(basket_3),
            {
                'sub-total': '£25.07',
                'discount': '£1.98',
                "total": '£23.09'
            }
        )

    def test_three_for_the_price_of_two(self):

        self.assertEqual(
            self.init_basket_pricer.handle({"Baked-Beans": 3}),
            {
                'sub-total': '£2.97',
                'discount': '£0.99',
                "total": '£1.98'
            }
        )

    def test_six_for_the_price_of_four(self):

        self.assertEqual(
            self.init_basket_pricer.handle({"Baked-Beans": 6}),
            {
                'sub-total': '£5.94',
                'discount': '£1.98',
                "total": '£3.96'
            }
        )

    def test_nine_for_the_price_of_six(self):

        self.assertEqual(
            self.init_basket_pricer.handle({"Baked-Beans": 9}),
            {
                'sub-total': '£8.91',
                'discount': '£2.97',
                "total": '£5.94'
            }
        )
        
    def test_new_offer_bonus_question(self):
        self.init_basket_pricer = BasketPricer(
            basket_4, catalogue, new_offer
        )

        self.assertEqual(
            self.init_basket_pricer.handle(basket_4),
            {
                'sub-total': '£17.00',
                'discount': '£5.50',
                "total": '£11.50'
            }
        )

    def test_my_new_offer_bonus_question(self):
        self.init_basket_pricer = BasketPricer(
            basket_3, catalogue, my_new_offer
        )

        self.assertEqual(
            self.init_basket_pricer.handle(basket_3),
            {
                'sub-total': '£25.07',
                'discount': '£2.99',
                "total": '£22.08'
            }
        )

    def test_basket_doesnt_match_catalogue(self):
        with self.assertRaises(Exception):
            self.init_basket_pricer.handle_items(basket_wrong_items)
