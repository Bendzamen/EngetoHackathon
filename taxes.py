
class Taxes:

    def __init__(self, interests_paid: list, max_discount: int = 150000):
        self.interests_paid: list = interests_paid
        self.max_discount = max_discount
        self.interests_yearly: list = []
        self.discounts: list = []
    
    def aggregate_yearly_values(self):
        months_in_year = 12
        for i in range(0, len(self.interests_paid), months_in_year):
            yearly_sum = sum(self.interests_paid[i:i+months_in_year])
            self.interests_yearly.append(yearly_sum)

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
    taxes = Taxes(interests, 1000)
    discounts = taxes.calculate_discounts()
    print(discounts)