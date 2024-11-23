from decimal import Decimal

from mortgage import Loan
from mortgage.loan import Installment

hypo_total = 100_000

p_a = 0.02
years = 2
refinancing_year = 1


class LoanWithRefinancing(Loan):
    def __init__(self, refinancing_year: int, refinancing_interest: float, *args, **kwargs):
        self.refinancing_year = refinancing_year
        self.refinancing_interest = refinancing_interest
        super().__init__(*args, **kwargs)

    def _amortize(self):
        initialize = Installment(
            number=0,
            payment=0,
            interest=0,
            principal=0,
            total_interest=0,
            balance=self.principal,
        )
        schedule = [initialize]
        total_interest = 0
        balance = self.principal
        for payment_number in range(1, self.term * self.n_periods + 1):

            # Refinancing
            if payment_number == self.refinancing_year * self.n_periods:
                self.interest = Decimal(self.refinancing_interest * 100) / 100
                balance = schedule[-1].balance
                total_interest = 0

            split = self.split_payment(payment_number, self._monthly_payment)
            interest_payment, principal_payment = split

            total_interest += interest_payment
            balance -= principal_payment
            installment = Installment(
                number=payment_number,
                payment=self._monthly_payment,
                interest=interest_payment,
                principal=principal_payment,
                total_interest=total_interest,
                balance=balance,
            )

            schedule.append(installment)

        return schedule


# Example
# loan = LoanWithRefinancing(principal=hypo_total, interest=p_a, term=years, currency="kč", refinancing_year=refinancing_year, refinancing_interest=0.06)

# loan.summarize

# for part in loan.schedule():
#    print(part)
