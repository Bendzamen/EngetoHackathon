class Taxes:

    def __init__(self, interests_paid: list, max_discount: int = 150000):
        self.tax_discounts: list = [i * 0.15 for i in interests_paid]
        self.max_discount = max_discount
        self.interests_yearly: list = []
        self.discounts: list = []

    def aggregate_yearly_values(self):
        months_in_year = 12
        for i in range(0, len(self.tax_discounts), months_in_year):
            yearly_sum = sum(self.tax_discounts[i : i + months_in_year])
            self.interests_yearly.append(round(yearly_sum, 2))

    def calculate_discounts(self):
        if not self.interests_yearly:
            self.aggregate_yearly_values()
        for i in self.interests_yearly:
            if i > self.max_discount:
                self.discounts.append(self.max_discount)
            else:
                self.discounts.append(i)
        return self.discounts


if __name__ == "__main__":
    interests = []
    for i in range(120):
        interests.append(i)
    taxes = Taxes(interests, 100)
    discounts = taxes.calculate_discounts()
    print(discounts)
