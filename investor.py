
class Investor:
    
    def __init__(self,
                 monthly_invest: float,
                 yearly_interest_rates: dict,
                 target_amount: float,
                 max_years: int):
        self.monthly_invest = monthly_invest
        self.yearly_interest_rates = yearly_interest_rates
        self.target_amount = target_amount
        self.max_years = max_years
        self.curr_val_risky = 0
        self.curr_val_medium = 0
        self.curr_val_safe = 0
        self.risky_reached = False
        self.medium_reached = False
        self.safe_reached = False

    def _apply_interests(self):
        self.curr_val_risky = self.curr_val_risky * (1 + self.yearly_interest_rates['risky'])
        self.curr_val_medium = self.curr_val_medium * (1 + self.yearly_interest_rates['medium'])
        self.curr_val_safe = self.curr_val_safe * (1 + self.yearly_interest_rates['safe'])

    def _add_investment(self):
        self.curr_val_risky += 12 * self.monthly_invest
        self.curr_val_medium += 12 * self.monthly_invest
        self.curr_val_safe += 12 * self.monthly_invest

    def _check_target_reached(self, years: int):
        if not self.risky_reached:
            if self.curr_val_risky >= self.target_amount:
                print(f'target reached with risky investments in {years} years') 
                self.risky_reached = True
        if not self.medium_reached:
            if self.curr_val_medium >= self.target_amount:
                print(f'target reached with medium investments in {years} years') 
                self.medium_reached = True
        if not self.safe_reached:
            if self.curr_val_safe >= self.target_amount:
                print(f'target reached with safe investments in {years} years') 
                self.safe_reached = True                

    def _final_check(self):
        if not self.risky_reached:
            print(f'risky target not reached in {self.max_years} years')
        if not self.medium_reached:
            print(f'medium target not reached in {self.max_years} years')
        if not self.safe_reached:
            print(f'safe target not reached in {self.max_years} years')


    def calculate_investments(self):
        for i in range(self.max_years):
            self._add_investment()
            self._apply_interests()
            self._check_target_reached(years=i)
        self._final_check()
        

if __name__ == "__main__":
    investor = Investor(monthly_invest=2000,
                        yearly_interest_rates={'risky': .08,
                                               'medium': .05,
                                               'safe': .03,},
                        target_amount=1000000,
                        max_years=30)
    investor.calculate_investments()
