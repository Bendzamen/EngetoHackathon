from collections import namedtuple

from mortgage import Loan


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

    def schedule_with_refinancing(self) -> list[namedtuple]:
        new_schedule = []
        for part in self.schedule():
            new_schedule.append(part)
            # Refinancing
            if part.number == self.n_periods * self.refinancing_year:
                new_loan = Loan(
                    principal=part.balance,
                    interest=self.refinancing_interest,
                    term=self.term - self.refinancing_year + self.new_hypo_length_change_years,
                )
                break


        for part in new_loan.schedule():
            print(part)
            new_schedule.append(part)

        return new_schedule


def main():
    # Example
    if 1:
        hypo_total = 100_000
        p_a = 0.02
        years = 2
        refinancing_year = 1
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
        length_change = -7

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

    for part in loan.schedule_with_refinancing():
        print(part)
        total_interest += part.interest
        total_principal += part.principal

    print(f"Total interest: {total_interest}")
    print(f"Total principal: {total_principal}")


if __name__ == "__main__":
    main()
