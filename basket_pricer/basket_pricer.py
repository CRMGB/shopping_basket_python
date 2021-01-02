import re
import math


class BasketPricer:
    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def handle(self, basket=None):
        if basket != None:
            self.basket = basket
        items_checked = self.handle_items(self.basket)
        basket_with_offers, discount = self.apply_offers(items_checked)
        return self.calcualte_result(basket_with_offers, discount)

    def handle_items(self, basket=None):
        basket_check = {
            item: basket[item]
            for item in self.catalogue
            if item in basket
        }
        wrong_items = self.basket.keys() - basket_check.keys()
        if wrong_items:
            raise ValueError(
                f"The item(s) {wrong_items} in the basket don't exists in the catalogue."
            )
        for item in basket_check:
            if basket_check[item] < 0:
                raise ValueError(
                    "Baskets cannot have a negative price."
                )
        return basket_check

    def apply_offers(self, basket_checked):
        discount = ''
        if self.offers and basket_checked:
            new_offer = {
                item: self.catalogue[item]
                for item, val in self.offers.items()
                if re.search(r'\bget the cheapest\b', val)
                and item in basket_checked
            }
            discount = [
                self.apply_offer_percentage(item, basket_checked)
                for item in self.offers
                if item in basket_checked
                and re.match(r'(\d+(\.\d+)?%)', self.offers[item])
            ]
            if len(discount) < 1 and not bool(new_offer):
                total_items_offer = [
                    self.apply_offer_items_free(item, val)
                    for item, val in self.offers.items()
                    if re.match(r'[buy]\w+', val) and item in basket_checked
                ]
                basket_checked = self.update_number_of_items_to_pay(
                    basket_checked, total_items_offer[0]
                )
            if new_offer:
                basket_checked = self.apply_new_offer(
                    new_offer, basket_checked)
        return basket_checked, discount

    def apply_offer_percentage(self, item, basket_checked):
        total_price_items = self.catalogue[item]*basket_checked[item]
        offer = int(self.offers[item].split("%")[0])
        return self.round_up(total_price_items * offer / 100, 2)

    def round_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

    def apply_offer_items_free(self, item, value):
        return {
            item: sum(list(
                int(i) for i in value.split()
                if i.isdigit()
            ))
        }

    def update_number_of_items_to_pay(self, basket_checked, total_offer):
        basket_checked.update({
            key: basket_checked[key] - round(basket_checked[key]/value)
            for key, value in total_offer.items()
            if key in basket_checked
        })
        return basket_checked

    def apply_new_offer(self, offer, basket_checked):
        min_items_offer_are_in_basket = {
            item: re.findall(r'[0-9]+', val)[0]
            for item, val in self.offers.items()
            if item in basket_checked
            and int(re.findall(r'[0-9]+', val)[0]) <= basket_checked[item]
        }
        items_wit_prices = self.total_amount_items(basket_checked, offer)
        if min_items_offer_are_in_basket:
            cheapest = min(items_wit_prices, key=items_wit_prices.get)
            most_expensive = max(items_wit_prices, key=items_wit_prices.get)
            return {
                (item if cheapest == item else item):
                (val-1 if item == cheapest
                 or most_expensive == item else val)
                for item, val in basket_checked.items()
            }

    def calcualte_result(self, basket_offer, discount):
        sub_total = self.total_amount_items(self.basket)
        total = self.total_amount_items(basket_offer)
        if len(discount) == 0:
            discount = sub_total-total
        else:
            total -= discount[-1]
            discount = discount[-1]

        return {
            "sub-total": f"£{sub_total}",
            "discount": f"£{round(discount, 2)}",
            "total": f"£{round(total, 2)}"
        }

    def total_amount_items(self, basket, offer=None):
        items_prices = {
            item: (self.catalogue[item] if offer
                   else basket[item]*self.catalogue[item])
            for item in self.catalogue
            if item in basket
        }
        return items_prices if offer else round(sum(items_prices.values()), 2)
