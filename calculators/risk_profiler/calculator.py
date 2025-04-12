def calculate_required_return(goal_amount, current_amount, time_horizon, monthly_savings):
    """
    Calculate the required annual return to reach the goal amount.
    """
    total_savings = monthly_savings * 12 * time_horizon
    future_value = goal_amount
    present_value = current_amount
    n = time_horizon
    pmt = monthly_savings * 12
    
    # Use the RATE function to calculate required return
    required_return = ((future_value - present_value) / (present_value + pmt * n)) * 100
    return round(required_return, 2)

def determine_risk_need(required_return):
    """
    Determine risk need based on required return.
    """
    if required_return > 8:
        return 'high'
    elif required_return > 4:
        return 'moderate'
    return 'low'

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
    
    # Calculate required return and risk need
    required_return = calculate_required_return(goal_amount, current_amount, time_horizon, monthly_savings)
    risk_need = determine_risk_need(required_return)
    
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
        'required_return': required_return,
        'risk_need': risk_need,
        'risk_ability': risk_ability,
        'behavioral_tolerance': behavioral_tolerance,
        'allocation': portfolio['allocation'],
        'equity_percentage': portfolio['equity_percentage'],
        'explanation': portfolio['explanation']
    } 