import re

class BasketPricer:
    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def handle(self, basket):
        items_checked = self.handle_items()
        basket_with_offers, items_with_offer = self.apply_offers(items_checked)
        return self.calcualte_total(basket_with_offers, items_with_offer)

    def handle_items(self, basket=None):
        if self.basket:
            if basket == None:
                basket = self.basket 
            basket_check = {
                item: basket[item]
                for item in self.catalogue
                if item in basket
            }
            wrong_items = basket.keys() - basket_check.keys()
            if wrong_items:
                raise ValueError(
                    f"The item(s) {wrong_items} in the basket don't exists in the catalogue."
                )
            for item in basket_check:
                if basket[item] < 0:
                    raise ValueError(
                        "Baskets cannot have a negative price."
                    )
            return basket_check
        else:
            return self.basket

    def apply_offers(self, basket_checked):
        offer = ''
        if self.offers and basket_checked:
            # Calculate free items
            for item, val in self.offers.items():
                if re.match(r'[buy]\w+', val):
                    total_offer = self.apply_offer_items_free(item, val)
            print("total_offer--> ", total_offer)
            print("self.basket--> ", self.basket)
            print("basket_checked--> ", basket_checked)
            basket_checked.update(self.update_price_with_offer(basket_checked, total_offer))
            # Calculate percentage
            for item in self.offers:
                if re.match(r'(\d+(\.\d+)?%)', self.offers[item]):
                    offer = self.apply_offer_percentage(item)
            print("basket_checked--> ", basket_checked)                    
            print("self.basket--> ", self.basket)

        return basket_checked, offer

    def apply_offer_items_free(self, item, value):
        return {
            item: sum(list(
                int(i) for i in value.split()
                if i.isdigit()
            ))
        }

    def update_price_with_offer(self, basket_checked, total_offer):
        return {
            key: basket_checked[key] - round(basket_checked[key]/value)
            for key, value in total_offer.items()
            if key in basket_checked
        }

    def apply_offer_percentage(self, item):
        offer = int(self.offers[item].split("%")[0])
        if item == next(reversed(self.offers.keys())):
            return {self.catalogue[item] - (self.catalogue[item] * offer / 100)}
            
    def calcualte_total(self, basket_offer, items_with_offer):
        sub_total = {
            item: self.basket[item]*self.catalogue[item]
            for item in self.catalogue
            if item in self.basket
        }
        total = {
            item: basket_offer[item]*self.catalogue[item]
            for item in self.catalogue
            if item in basket_offer
        }
        return {
            "sub-total": f"£{round(sum(sub_total.values()), 2)}",
            "offer": self.offers,
            "total": f"£{round(sum(total.values()), 2)}"
        }
