import re

class BasketPricer:
    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def handle(self):
        items_checked = self.handle_items()
        items_with_offer = self.apply_offers(items_checked)
        return self.calcualte_total(items_checked, items_with_offer)

    def handle_items(self):
        if self.basket:
            basket = {
                    item: self.basket[item]
                    for item in self.catalogue
                    if item in self.basket
                }
            if not basket:
                raise ValueError(
                    "The items in basket don't exists in the catalogue"
                )
            return basket           
        else:
            return self.basket

    def apply_offers(self, basket):
        if self.offers:
            offer = {
                    item: self.offers[item]
                    for item in self.catalogue
                    if item in self.offers
                }
            if not offer:
                raise ValueError(
                    "No offer for the items in the basket has been found"
                )
                # Do something with offer
            return basket
        else:
            return basket

    def calcualte_total(self, items_checked, items_with_offer):
        #Still need to implement the offer
        basket_sub_total = {
                item: items_checked[item]*self.catalogue[item]
                for item in self.catalogue
                if item in items_checked
            }
        return {
                "sub-total": sum(basket_sub_total.values()),
                "offer": self.offers,
                "total": sum(basket_sub_total.values())
            }
