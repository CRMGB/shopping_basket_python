import re

class BasketPricer:
    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def handle(self):
        items_checked = self.handle_items()
        basket_with_offers, items_with_offer = self.apply_offers(items_checked)
        return self.calcualte_total(basket_with_offers, items_with_offer)

    def handle_items(self):
        if self.basket:
            basket = {
                item: self.basket[item]
                for item in self.catalogue
                if item in self.basket
            }
            wrong_items = self.basket.keys() - basket.keys()
            if wrong_items:
                raise ValueError(
                    f"The item(s) {wrong_items} in the basket don't exists in the catalogue"
                )
            for item in basket:
                if basket[item] < 0:
                    raise ValueError(
                        "Baskets cannot have a negative price."
                    )
            return basket
        else:
            return self.basket

    def apply_offers(self, basket):
        offer = ''
        if self.offers and basket:
            # Calculate free items
            for item, val in self.offers.items():
                if re.match(r'[buy]\w+', val):
                    total_offer = self.apply_offer_items_free(item, val)

            for key, value in total_offer.items():
                if key in basket:
                    basket[key] = basket[key] - round(basket[key]/value)

            # Calculate percentage
            for item in self.offers:
                if re.match(r'(\d+(\.\d+)?%)', self.offers[item]):
                    offer = self.apply_offer_percentage(item)

        return basket, offer

    def apply_offer_items_free(self, item, value):
        return {
            item: sum(list(
                int(i) for i in value.split()
                if i.isdigit()
            ))
        }

    def apply_offer_percentage(self, item):
        offer = int(self.offers[item].split("%")[0])
        if item == next(reversed(self.offers.keys())):
            return {self.catalogue[item] - (self.catalogue[item] * offer / 100)}
            

    def calcualte_total(self, basket, items_with_offer):
        sub_total = {
            item: self.basket[item]*self.catalogue[item]
            for item in self.catalogue
            if item in self.basket
        }
        total = {
            item: basket[item]*self.catalogue[item]
            for item in self.catalogue
            if item in basket
        }
        return {
            "sub-total": f"£{round(sum(sub_total.values()), 2)}",
            "offer": self.offers,
            "total": f"£{round(sum(total.values()), 2)}"
        }
