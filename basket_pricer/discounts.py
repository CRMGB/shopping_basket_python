import math
import re

class DiscountClass:
    def __init__(self, new_offer, basket_checked, offers, catalogue):
        self.new_offer = new_offer
        self.basket_checked = basket_checked
        self.offers = offers
        self.catalogue = catalogue

    def basket_with_discount(self):
        discount = self.__check_discount(self.basket_checked)
        if len(discount) < 1 and not bool(self.new_offer):
            total_items_offer = [
                self.__apply_offer_items_free(item, val)
                for item, val in self.offers.items()
                if re.match(r'[buy]\w+', val) and item in self.basket_checked
            ]
            self.basket_checked = self.__update_number_of_items_to_pay(
                self.basket_checked, total_items_offer
            )
        return self.basket_checked, discount

    def __check_discount(self, basket_checked):
        return [
            self.__apply_offer_percentage(item, basket_checked)
            for item in self.offers
            if item in basket_checked
            and re.match(r'(\d+(\.\d+)?%)', self.offers[item])
        ]

    def __apply_offer_items_free(self, item, value):
        return {
            item: sum(list(int(i) for i in value.split()
                if i.isdigit()
            ))
        }

    def __apply_offer_percentage(self, item, basket_checked):
        total_price_items = self.catalogue[item]*basket_checked[item]
        offer = int(self.offers[item].split("%")[0])
        return self.__round_up(total_price_items * offer / 100, 2)

    def __round_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

    def __update_number_of_items_to_pay(self, basket_checked, total_offer):
        if len(total_offer)>0:
            basket_checked.update({
                key: basket_checked[key] - round(basket_checked[key]/value)
                for key, value in total_offer[0].items()
                if key in basket_checked
            })
        return basket_checked