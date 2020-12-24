import re


class BasketPricer:
    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def handle(self, basket=None):
        if basket != None:
            self.basket = basket
        items_checked = self.handle_items(basket)
        basket_with_offers = self.apply_offers(items_checked)
        return self.calcualte_result(basket_with_offers)

    def handle_items(self, basket=None):
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

    def apply_offers(self, basket_checked):
        offer = ''
        if self.offers and basket_checked:

            # Calculate percentage
            for item in self.offers:
                if re.match(r'(\d+(\.\d+)?%)', self.offers[item]):
                    if item in basket_checked:
                        offer = self.apply_offer_percentage(item)
            # Calculate free items
            if offer == '':
                for item, val in self.offers.items():
                    if re.match(r'[buy]\w+', val):
                        if item in basket_checked:
                            total_offer = self.apply_offer_items_free(
                                item, val)

                basket_checked = self.update_price_with_offer(
                    basket_checked, total_offer)

        return basket_checked

    def apply_offer_items_free(self, item, value):
        return {
            item: sum(list(
                int(i) for i in value.split()
                if i.isdigit()
            ))
        }

    def update_price_with_offer(self, basket_checked, total_offer):
        basket_checked.update({
            key: basket_checked[key] - round(basket_checked[key]/value)
            for key, value in total_offer.items()
            if key in basket_checked
        })
        return basket_checked

    def apply_offer_percentage(self, item):
        offer = int(self.offers[item].split("%")[0])
        if item == next(reversed(self.offers.keys())):
            return {self.catalogue[item] - (self.catalogue[item] * offer / 100)}

    def calcualte_result(self, basket_offer):
        sub_total = self.calcualte_sub_total_and_total(self.basket)
        total = self.calcualte_sub_total_and_total(basket_offer)

        sub_total = round(sum(sub_total.values()), 2)
        total = round(sum(total.values()), 2)
        return {
            "sub-total": f"£{sub_total}",
            "discount": f"£{round(sub_total-total, 2)}",
            "total": f"£{total}"
        }

    def calcualte_sub_total_and_total(self, basket):
        return {
            item: basket[item]*self.catalogue[item]
            for item in self.catalogue
            if item in basket
        }
