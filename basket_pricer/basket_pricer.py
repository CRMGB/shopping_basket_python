import re

class BasketPricer:
    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def get_basket_and_catalogue(self):

        basket = {item: self.basket[item]
                 for item in self.catalogue
                 if item in self.basket
                }
        if basket:
            self.apply_offers(basket)
        else:
            raise ValueError(
                "The items in basket don't exists in the catalogue"
            )

    def apply_offers(self, basket):
        value = {item: self.offers[item]
                 for item in basket
                 if item in self.offers
                }
        if value:
            # Do something with offer
            print(f'The values-->{value}')
        else:
            raise ValueError(
                "No offer for the items in the basket has been found"
            )