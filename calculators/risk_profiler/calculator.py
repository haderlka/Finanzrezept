def calculate_required_return(target_value, current_value, time_horizon_years, monthly_savings, equity_return, bonds_return):
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

    return round(equity_allocation, 2)

def determine_risk_need(required_alloc):
    """
    Determine risk need based on required return.
    """
    if required_alloc < 30:
        return 'low'
    elif required_alloc <= 70:
        return 'moderate' 
    else:
        return 'high'

def determine_risk_ability(preservation_importance, income_ratio):
    """
    Determine risk-taking ability based on preservation importance and income ratio.
    """
    if preservation_importance == 'high' or income_ratio == 'low':
        return 'low'
    elif preservation_importance == 'low' and income_ratio == 'high':
        return 'high'
    return 'moderate'

def calculate_behavioral_tolerance(financial_knowledge, market_reaction, market_risk_perception):
    """
    Calculate behavioral loss tolerance based on various factors.
    """
    knowledge_score = {'high': 3, 'medium': 2, 'low': 1}[financial_knowledge]
    reaction_score = {'hold': 3, 'sell': 1, 'buy': 5}[market_reaction]
    perception_score = {'high': 1, 'medium': 3, 'low': 5}[market_risk_perception]
    
    total_score = knowledge_score + reaction_score + perception_score
    
    if total_score >= 9:
        return 'high'
    elif total_score >= 6:
        return 'moderate'
    return 'low'

def determine_portfolio_allocation(risk_need, risk_ability, behavioral_tolerance):
    """
    Determine the recommended portfolio allocation based on risk factors.
    """
    if risk_need == 'high' and risk_ability == 'high' and behavioral_tolerance == 'high':
        return {
            'allocation': 'high',
            'equity_percentage': 70,
            'explanation': "Ihr Profil zeigt eine hohe Risikobereitschaft und -fähigkeit. Eine hohe Aktienquote ist angemessen."
        }
    elif risk_need == 'moderate' and risk_ability == 'moderate' and behavioral_tolerance == 'moderate':
        return {
            'allocation': 'moderate',
            'equity_percentage': 50,
            'explanation': "Ihr Profil zeigt eine moderate Risikobereitschaft. Eine ausgewogene Mischung ist empfehlenswert."
        }
    else:
        return {
            'allocation': 'low',
            'equity_percentage': 30,
            'explanation': "Ihr Profil zeigt eine konservative Risikoneigung. Eine defensive Anlagestrategie ist ratsam."
        }

def calculate_risk_profile(form_data):
    """
    Calculate the complete risk profile based on form data.
    """
    # Extract form data
    goal_amount = float(form_data.get('goal_amount', 0))
    current_amount = float(form_data.get('current_amount', 0))
    time_horizon = float(form_data.get('time_horizon', 0))
    monthly_savings = float(form_data.get('monthly_savings', 0))
    equity_return = float(form_data.get('expected_stock_return', 0))
    bonds_return = float(form_data.get('expected_safe_return', 0))
    
    # Calculate required return and risk need
    required_equity_rate = calculate_required_return(goal_amount, current_amount, time_horizon, monthly_savings, equity_return, bonds_return)
    risk_need = determine_risk_need(required_equity_rate)
    
    # Determine risk ability
    preservation_importance = form_data.get('preservation_importance')
    income_ratio = form_data.get('income_ratio')
    risk_ability = determine_risk_ability(preservation_importance, income_ratio)
    
    # Calculate behavioral tolerance
    financial_knowledge = form_data.get('financial_knowledge')
    market_reaction = form_data.get('market_reaction')
    market_risk_perception = form_data.get('market_risk_perception')
    behavioral_tolerance = calculate_behavioral_tolerance(
        financial_knowledge, market_reaction, market_risk_perception
    )
    
    # Determine portfolio allocation
    portfolio = determine_portfolio_allocation(risk_need, risk_ability, behavioral_tolerance)
    
    return {
        'required_equity_rate': required_equity_rate,
        'risk_need': risk_need,
        'risk_ability': risk_ability,
        'behavioral_tolerance': behavioral_tolerance,
        'allocation': portfolio['allocation'],
        'equity_percentage': portfolio['equity_percentage'],
        'explanation': portfolio['explanation']
    } 