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

        for part in new_loan.schedule():
            self.new_monthly_payment = part.payment
            new_installment = Installment.from_namedtuple(part)
            new_installment.monthly_payment_difference = self.new_monthly_payment - self.original_monthly_payment
            new_schedule.append(new_installment)

        if self.monthly_payment_difference_after_refinancing > 0:
            # Investment part
            invest_data = InvestmentData()
            investor = Investor(
                invest_data=invest_data,
                monthly_invest=float(self.monthly_payment_difference_after_refinancing),
                yearly_interest_rates={
                    "risky": 0.08,  # add couple % to S&P?
                    "medium": 0.05,  # take from S&P index
                    "safe": 0.03,  # state bonds
                },
                target_amount=self.new_loan.principal,
                max_years=self.years_from_refinancing_to_end,
            )
            print(repr(investor.__dict__))
            invest_data = investor.calculate_investments()
            print("list of risky investment values")
            for i, val in enumerate(invest_data.risky_values):
                print(f"year: {i + 1}, value: {val}")
            print("list of medium investment values")
            for i, val in enumerate(invest_data.medium_values):
                print(f"year: {i + 1}, value: {val}")
            print("list of safe investment values")
            for i, val in enumerate(invest_data.safe_values):
                print(f"year: {i + 1}, value: {val}")

            break_free = False
            for year in range(self.years_from_refinancing_to_end):
                print(f"Year: {year + 1}")
                print(f"Risky: {invest_data.risky_values[year]}")
                print(f"Medium: {invest_data.medium_values[year]}")
                print(f"Safe: {invest_data.safe_values[year]}")
                print()
                start_year = year + self.refinancing_year
                print(start_year)
                for part in new_schedule[start_year * 12 : start_year * 12 + 12]:
                    part.investment_values = {}
                    part.investment_values["risky"] = invest_data.risky_values[year]
                    part.investment_values["medium"] = invest_data.medium_values[year]
                    part.investment_values["safe"] = invest_data.safe_values[year]
                    print(part)
                    if part.balance < part.investment_values["risky"]:
                        print("-" * 50)
                        print("Investment reached the balance")
                        break_free = True
                        break

                if break_free:
                    break

        return new_schedule

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
