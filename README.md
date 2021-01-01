SHOPPING BASKET PYTHON

Im doing TDD developent based on the assignment.md which means every point from the "Behavior" section in the assignment.md should be tested from the unittest file:
    - basket_pricer/basket_pricer_test/test_basket_pricer.py

To run such tests I'm using python unittest with the command from basket_pricer/basket_pricer_tests: "python -m unittest test_basket_pricer.BasketPricerTest"

I've tried the minimal amount of test to show my code works so I don't create a large file but obviously you can add more cases and they should pass.

There is a consideration for the error management raising Value Error as well as testing it.

No hardcoded data has been set as the assignment suggests but there are a few dictionaries for testing purposes in the test_basket_pricer.py in the simplest way and sticking to the examples.

The bonus question 1 is done with the test "test_new_offer_bonus_question" which I only used a new dictionary and a method called "apply_new_offer" inside of "new_offer" function but I rehuse the rest of the code from previous points to get the result.

The "apply_new_offer" is a large method but very straight forward, first detects the minimum items to complete de offer, then checks whether they are in the basket, gets the prices from the items in basket to calculate the cheapest and most expensive item and finally generates a new basket without the free items (or only the itmes to pay) 

I did perform 3 extra tests not mentioned in the assignment (2 are normal successfull transactions and one of them is with another version of the bonus question)

The python version used is 3.8.5 with virtual environment but the code used should be good to go in previous versions of python 3.