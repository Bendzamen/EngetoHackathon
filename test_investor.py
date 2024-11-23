from investor import Investor, InvestmentData


def init_investor():
    invest_data = InvestmentData()
    monthly_invest = 1000
    yearly_interest_rates = {
        "risky": 0.08,
        "medium": 0.05,
        "safe": 0.03,
    }
    target_amount = 1000000
    max_years = 30

    investor = Investor(
        invest_data=invest_data,
        monthly_invest=monthly_invest,
        yearly_interest_rates=yearly_interest_rates,
        target_amount=target_amount,
        max_years=max_years,
    )
    return investor


def test_calculate_investments():
    investor = init_investor()
    invest_data = investor.calculate_investments()

    assert invest_data.risky_values[2] == 42073
    assert invest_data.medium_values[2] == 39721
    assert invest_data.safe_values[2] == 38203
    assert investor.risky_reached
    assert not investor.medium_reached
    assert not investor.safe_reached
