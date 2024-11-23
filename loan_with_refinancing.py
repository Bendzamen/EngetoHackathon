from collections import namedtuple
from dataclasses import dataclass

from mortgage import Loan

from investor import InvestmentData, Investor


@dataclass
class Installment:
    number: int
    payment: float
    principal: float
    interest: float
    total_interest: float
    balance: float
    monthly_payment_difference: float = 0.0
    investment_values: dict[str, float] = None

    @staticmethod
    def from_namedtuple(installment: namedtuple):
        return Installment(
            number=installment.number,
            payment=installment.payment,
            principal=installment.principal,
            interest=installment.interest,
            total_interest=installment.total_interest,
            balance=installment.balance,
            monthly_payment_difference=0.0,
            investment_values=None,
        )


class LoanWithRefinancing(Loan):
    def __init__(
        self,
        refinancing_year: int,
        refinancing_interest: float,
        new_hypo_length_change_years: int,
        *args,
        **kwargs,
    ):
        self.refinancing_year = refinancing_year
        self.refinancing_interest = refinancing_interest
        self.new_hypo_length_change_years = new_hypo_length_change_years
        super().__init__(*args, **kwargs)
        self.original_monthly_payment = 0
        self.new_monthly_payment = 0
        self.new_loan = None

    def schedule_with_refinancing(self) -> list[namedtuple]:
        new_schedule = []
        for part in self.schedule():
            self.original_monthly_payment = part.payment
            new_installment = Installment.from_namedtuple(part)
            new_schedule.append(new_installment)
            # Refinancing
            if part.number == self.n_periods * self.refinancing_year:
                new_loan = Loan(
                    principal=part.balance,
                    interest=self.refinancing_interest,
                    term=self.term - self.refinancing_year + self.new_hypo_length_change_years,
                )
                self.new_loan = new_loan
                break

        invest_data = InvestmentData()
        investor = None
        first = True
        for part in new_loan.schedule():
            if part.number == 0:
                continue
            self.new_monthly_payment = part.payment
            new_installment = Installment.from_namedtuple(part)
            new_installment.monthly_payment_difference = self.new_monthly_payment - self.original_monthly_payment
            if first:
                investor = Investor(
                    invest_data=invest_data,
                    monthly_invest=float(new_installment.monthly_payment_difference),
                    yearly_interest_rates={
                        "risky": 0.08,  # add couple % to S&P?
                        "medium": 0.05,  # take from S&P index
                        "safe": 0.03,  # state bonds
                    },
                )
                first = False
            new_investment_data = investor.add_investment()
            new_installment.investment_values = {
                "risk": new_investment_data[0],
                "medium": new_investment_data[1],
                "safe": new_investment_data[2],
            }
            new_schedule.append(new_installment)

        if self.monthly_payment_difference_after_refinancing > 0:
            # Investment part
            invest_data = InvestmentData()
            print("list of risky investment values")
            for i, val in enumerate(invest_data.risky_values):
                print(f"year: {i + 1}, value: {val}")
            print("list of medium investment values")
            for i, val in enumerate(invest_data.medium_values):
                print(f"year: {i + 1}, value: {val}")
            print("list of safe investment values")
            for i, val in enumerate(invest_data.safe_values):
                print(f"year: {i + 1}, value: {val}")

        return new_schedule[1:]

    @property
    def years_from_refinancing_to_end(self):
        return self.term - self.refinancing_year + self.new_hypo_length_change_years

    @property
    def monthly_payment_difference_after_refinancing(self):
        return self.new_monthly_payment - self.original_monthly_payment


def main():
    # Example
    if 1:
        hypo_total = 100_000
        p_a = 0.02
        years = 20
        refinancing_year = 10
        refinancing_p_a = 0.1
        length_change = 0

    if 0:
        hypo_total = 200_000
        p_a = 0.02
        years = 2
        refinancing_year = 1
        refinancing_p_a = 0.1
        length_change = 0

    if 0:
        hypo_total = 2_500_000
        p_a = 0.0169
        years = 30
        refinancing_year = 7
        refinancing_p_a = 0.0564
        length_change = 7

    loan = LoanWithRefinancing(
        principal=hypo_total,
        interest=p_a,
        term=years,
        refinancing_year=refinancing_year,
        refinancing_interest=refinancing_p_a,
        new_hypo_length_change_years=length_change,
    )

    total_interest = 0
    total_principal = 0
    monthly_schedule = loan.schedule_with_refinancing()

    for part in monthly_schedule:
        print(part)
        total_interest += part.interest
        total_principal += part.principal

    print(f"Total interest: {total_interest}")
    print(f"Total principal: {total_principal}")
    print(f"Original monthly payment: {loan.original_monthly_payment}")
    print(f"New monthly payment: {loan.new_monthly_payment}")


if __name__ == "__main__":
    main()
