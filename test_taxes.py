from taxes import Taxes


def init_taxes():
    interests = []
    for i in range(120):
        interests.append(i)
    max_discount = 100
    taxes = Taxes(interests_paid=interests, max_discount=100)
    return taxes


def test_aggregate_yearly_values():
    taxes = init_taxes()
    taxes.aggregate_yearly_values()
    assert taxes.interests_yearly[0] == 9.9
    assert taxes.interests_yearly[9] == 204.3


def test_calculate_discounts():
    taxes = init_taxes()
    discounts = taxes.calculate_discounts()
    assert discounts[0] == 9.9
    assert discounts[9] == 100
