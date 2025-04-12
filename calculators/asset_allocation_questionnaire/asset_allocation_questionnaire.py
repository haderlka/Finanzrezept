from ..generic.constants import EXPECTED_REAL_RATE_OF_EQUITY_RETURN, EXPECTED_REAL_RATE_OF_BONDS_RETURN

class Rating(Enum):
    NOT_RATED = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Questionnaire:
    def __init__(self):
        self.risk_need = Rating.NOT_RATED
        self.risk_need_equity_allocation = None
        self.risk_ability_time_horizon = Rating.NOT_RATED
        self.risk_ability_liquidity_need = Rating.NOT_RATED
        self.risk_ability_capacity = Rating.NOT_RATED

    def eval_risk_need(self, equity_allocation):
        self.risk_need_equity_allocation = equity_allocation
        if equity_allocation < 30:
            self.risk_need = Rating.LOW
        elif equity_allocation <= 70:
            self.risk_need =  Rating.MEDIUM 
        else:
            self.risk_need =  Rating.HIGH


#1. section of the questionnaire: "Risikonotwendigkeit"
def risk_need_questionnaire(current_value, time_horizon_years, monthly_savings, target_value, equity_return=EXPECTED_REAL_RATE_OF_EQUITY_RETURN, bonds_return=EXPECTED_REAL_RATE_OF_BONDS_RETURN):
    """
    Calculate the risk need of an investor.

    Uses EXPECTED_REAL_RATE_OF_RETURN for risky assets and EXPECTED_REAL_RATE_OF_BONDS_RETURN for bonds / safe assets.
    The risk need is calculated as the percentage of the money allocated to equity.
    
    Args:
        current_value (str): The current value of the investor's portfolio
        time_horizon_years (str): The time horizon of the investor's investment
        monthly_savings (str): The monthly savings of the investor -> Can also be negative
        target_value (str): The target value of the investor's portfolio
        
    Returns:
        float: The percentage of the portfolio that should be allocated to equity
    """
    # Convert inputs to float
    qa_data = Questionnaire()

    current_value = float(current_value)
    time_horizon_years = float(time_horizon_years)
    monthly_savings = float(monthly_savings)
    target_value = float(target_value)
    
    # Convert annual rates to monthly rates
    equity_monthly_rate = (1 + equity_return/100) ** (1/12) - 1
    bond_monthly_rate = (1 + bonds_return/100) ** (1/12) - 1
    
    # Calculate total number of months
    total_months = time_horizon_years * 12
    
    # Calculate future value of current portfolio with 100% equity
    equity_fv = current_value * (1 + equity_monthly_rate) ** total_months
    
    # Calculate future value of current portfolio with 100% bonds
    bond_fv = current_value * (1 + bond_monthly_rate) ** total_months
    
    # Calculate future value of monthly contributions with 100% equity
    equity_contributions_fv = 0
    for month in range(int(total_months)):
        equity_contributions_fv += monthly_savings * (1 + equity_monthly_rate) ** (total_months - month)
    
    # Calculate future value of monthly contributions with 100% bonds
    bond_contributions_fv = 0
    for month in range(int(total_months)):
        bond_contributions_fv += monthly_savings * (1 + bond_monthly_rate) ** (total_months - month)
    
    # Calculate total future values
    total_equity_fv = equity_fv + equity_contributions_fv
    total_bond_fv = bond_fv + bond_contributions_fv
    
    # If target value is less than or equal to bond future value, no equity needed
    if target_value <= total_bond_fv:
        return 0.0
    
    # If target value is greater than or equal to equity future value, 100% equity needed
    if target_value >= total_equity_fv:
        return 100.0
    
    # Calculate required equity allocation using linear interpolation
    equity_allocation = ((target_value - total_bond_fv) / (total_equity_fv - total_bond_fv)) * 100

    qa_data.eval_risk_need(equity_allocation)

    return round(equity_allocation, 2)



#2. section of the questionnaire: "Risikotragfähigkeit"


#1. section of the questionnaire: "Risikobereitschaft"