import re
from discounts import DiscountClass

class BasketPricer:
    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def handle(self, basket=None):
        if basket != None:
            self.basket = basket
        items_checked = self.handle_items(self.basket)
        basket_with_offers, discount = self.__apply_offers(items_checked)
        return self.__calcualte_result(basket_with_offers, discount)

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

    def __apply_offers(self, basket_checked):

        new_offer = self.__check_whether_new_offers(basket_checked)

        init_discount = DiscountClass(
            new_offer, basket_checked, self.offers, self.catalogue
        )

        basket_checked, discount = init_discount.basket_with_discount()

        if new_offer:
            basket_checked = self.__apply_new_offer(
                new_offer, basket_checked
            )
        return basket_checked, discount

    def __check_whether_new_offers(self, basket_checked):
        if self.offers and basket_checked:
            return {
                item: self.catalogue[item]
                for item, val in self.offers.items()
                if re.search(r'\bget the cheapest\b', val)
                and item in basket_checked
            }
    
    def __apply_new_offer(self, offer, basket_checked):

        items_with_prices = self.__total_amount_items(basket_checked, offer)
        if self.__min_items_offer_are_in_basket(basket_checked):
            cheapest = min(items_with_prices, key=items_with_prices.get)
            most_expensive = max(items_with_prices, key=items_with_prices.get)
            return {
                (item if cheapest == item else item):
                (val-1 if item == cheapest
                 or most_expensive == item else val)
                for item, val in basket_checked.items()
            }

    def __min_items_offer_are_in_basket(self, basket_checked):
        return {
            item: re.findall(r'[0-9]+', val)[0]
            for item, val in self.offers.items()
            if item in basket_checked
            and int(re.findall(r'[0-9]+', val)[0]) <= basket_checked[item]
        }

    def __calcualte_result(self, basket_offer, discount):
        sub_total = self.__total_amount_items(self.basket)
        total = self.__total_amount_items(basket_offer)
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

    def __total_amount_items(self, basket, offer=None):
        items_prices = {
            item: (self.catalogue[item] if offer
                   else basket[item]*self.catalogue[item])
            for item in self.catalogue
            if item in basket
        }
        return items_prices if offer else round(sum(items_prices.values()), 2)
