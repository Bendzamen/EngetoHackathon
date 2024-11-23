from decimal import Decimal

from loan_with_refinancing import LoanWithRefinancing


def test_loan_with_refinancing():
    hypo_total = 100_000
    p_a = 0.01
    years = 2
    refinancing_year = 1
    refinancing_p_a = 0.1
    length_change = 0

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

    assert int(total_principal) == Decimal(100_000.0)
    assert total_interest == Decimal("3535.664373251231795866491537")

    print(f"Total interest: {total_interest}")
    print(f"Total principal: {total_principal}")
