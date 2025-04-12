from decimal import Decimal, ROUND_DOWN

def calculate_compound_interest(initial_amount, monthly_contribution, annual_interest_rate, years):
    """
    Calculate compound interest with monthly contributions.
    
    Args:
        initial_amount (float): Initial investment amount
        monthly_contribution (float): Monthly contribution amount
        annual_interest_rate (float): Annual interest rate in percentage
        years (int): Number of years
        
    Returns:
        dict: Dictionary containing total amount, total contributions, and interest earned
    """
    # Convert inputs to Decimal for precise calculations
    initial_amount = Decimal(str(initial_amount))
    monthly_contribution = Decimal(str(monthly_contribution))
    monthly_rate = Decimal(str(annual_interest_rate)) / Decimal('1200')  # Convert annual rate to monthly
    months = years * 12
    
    # Calculate future value
    future_value = initial_amount * (1 + monthly_rate) ** months
    future_value += monthly_contribution * ((1 + monthly_rate) ** months - 1) / monthly_rate
    
    # Calculate total contributions
    total_contributions = initial_amount + (monthly_contribution * months)
    
    # Calculate interest earned
    interest_earned = future_value - total_contributions
    
    # Round to 2 decimal places
    future_value = future_value.quantize(Decimal('.01'), rounding=ROUND_DOWN)
    total_contributions = total_contributions.quantize(Decimal('.01'), rounding=ROUND_DOWN)
    interest_earned = interest_earned.quantize(Decimal('.01'), rounding=ROUND_DOWN)
    
    return {
        'future_value': float(future_value),
        'total_contributions': float(total_contributions),
        'interest_earned': float(interest_earned)
    } 