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
    # if target_value >= total_equity_fv:
    #     return 100.0
    
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
    elif required_alloc <= 100:
        return 'high'
    else:
        return 'too high'

def determine_risk_ability(additional_benefits, monthly_savings, time_horizon):
    """
    Determine risk-taking ability
    """
    text = ""
    res = ''
    if time_horizon <= 5:
        res = 'low'
        text = "Dein Zeithorizont ist zu kurz für eine hohe Aktienquote."
    elif (additional_benefits == 'low' and monthly_savings <= 0):
        res = 'low'
        text = "Du hast zu wenig Absicherung neben deinem Investment für eine hohe Aktienquote. Auch deine Sparrate ist zu gering um als Puffer zu dienen."
    elif time_horizon >=10 and (additional_benefits == 'high' or monthly_savings >= 1000):
        res = 'high'
        text = "Du hast einen langen Zeithorizont und kannst über zusätzliche Absicherung oder aussetzen der Sparrate schlechte Zeiten überbrücken."
    else:
        res = 'moderate'
        if time_horizon < 10:
            text = "Du hast einen mittleren Zeithorizont"
        else:
            text = "Du hast einen langen Zeithorizont, aber in schwierigen Zeiten wenig Puffer über deine Sparrate oder zusätzliche Absicherung."
    return res, text

def determine_behavioral_tolerance(answers):
    """
    Determine the behavioral risk tolerance based on the questionnaire answers.
    
    Args:
        answers: Dictionary containing answers to behavioral questions
        
    Returns:
        str: Risk tolerance level ('high', 'moderate', 'low', 'very_low')
    """
    # Calculate total score
    behavioral_tolerance_text = ""
    total_score = 0
    result = ""
    
    # Question 1: Risk taker description
    total_score += int(answers.get('behavioral_question1', 0))
    
    # Question 2: Game show choice
    total_score += int(answers.get('behavioral_question2', 0))
    
    # Question 3: Vacation decision
    total_score += int(answers.get('behavioral_question3', 0))
    
    # Question 4: 20k investment choice
    total_score += int(answers.get('behavioral_question4', 0))
    
    # Question 5: Comfort with stocks
    total_score += int(answers.get('behavioral_question5', 0))
    
    # Question 6: Risk word association
    total_score += int(answers.get('behavioral_question6', 0))
    
    # Question 8: Investment choice with best/worst case
    total_score += int(answers.get('behavioral_question8', 0))
    
    # Question 9: Sure gain vs chance
    total_score += int(answers.get('behavioral_question9', 0))
    
    # Question 10: Sure loss vs chance
    total_score += int(answers.get('behavioral_question10', 0))
    
    # Question 11: 100k inheritance investment
    total_score += int(answers.get('behavioral_question11', 0))
    
    # Question 12: 20k portfolio allocation
    total_score += int(answers.get('behavioral_question12', 0))
    
    # Question 13: Gold mine investment
    total_score += int(answers.get('behavioral_question13', 0))
    
    # Determine risk level based on total score
    if total_score >= 29:
        result = 'high'
        behavioral_tolerance_text = "Du gehst gerne Risiken ein"
    elif total_score >= 19:
        result = 'moderate'
        behavioral_tolerance_text = "Du kannst Risiken eingehen, wenn es dir sinnvoll erscheint."
    elif total_score >= 15:
        result = 'low'
        behavioral_tolerance_text = "Du gehst nicht gerne Risiken ein"
    else:
        result = 'very_low'
        behavioral_tolerance_text = "Risiken und Unsicherheit machen dir Angst."
    return result, behavioral_tolerance_text

def determine_portfolio_allocation(risk_need, risk_ability, behavioral_tolerance):
    """
    Determine the recommended portfolio allocation based on risk factors.
    """
    if risk_ability == 'low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 0,
            'explanation': "Du hast nicht die Risikotragfähigkeit um in Aktien zu investieren."
        }
    elif risk_ability == 'moderate' and risk_need == 'low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 0,
            'explanation': "Du hast nicht die Notwendigkeit in Aktien zu investieren."
        }  
    elif risk_ability == 'moderate' and risk_need == 'moderate' and behavioral_tolerance == 'very_low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 0,
            'explanation': "Du hast nicht die Risikotoleranz um in Aktien zu investieren."
        }  
    elif risk_ability == 'moderate' and risk_need == 'moderate' and behavioral_tolerance == 'low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 10,
            'explanation': "Du kannst ein bisschen in Aktien investieren auch um deine Risikotoleranz zu verbessern."
        }  
    elif risk_ability == 'moderate' and risk_need == 'moderate' and behavioral_tolerance == 'moderate':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 20,
            'explanation': ""
        } 
    elif risk_ability == 'moderate' and risk_need == 'moderate' and behavioral_tolerance == 'moderate':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 30,
            'explanation': ""
        } 
    elif risk_ability == 'moderate' and (risk_need == 'high' or 'too high') and behavioral_tolerance == 'very_low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 10,
            'explanation': "Du kannst ein bisschen in Aktien investieren auch um deine Risikotoleranz zu verbessern."
        } 
    elif risk_ability == 'moderate' and (risk_need == 'high' or 'too high') and behavioral_tolerance == 'low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 20,
            'explanation': "Du kannst ein bisschen in Aktien investieren auch um deine Risikotoleranz zu verbessern."
        } 
    elif risk_ability == 'moderate' and (risk_need == 'high' or 'too high') and behavioral_tolerance == 'moderate':
        return {
            'allocation': 'Mittel',
            'equity_percentage': 40,
            'explanation': ""
        } 
    elif risk_ability == 'moderate' and (risk_need == 'high' or 'too high') and behavioral_tolerance == 'high':
        return {
            'allocation': 'Mittel',
            'equity_percentage': 50,
            'explanation': ""
        } 
    elif risk_ability == 'high' and risk_need == 'low' and behavioral_tolerance == 'very_low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 0,
            'explanation': "Du hast nicht die Notwendigkeit dich trotz niedrieger Risikotoleranz in Aktien zu investieren."
        } 
    elif risk_ability == 'high' and risk_need == 'low' and behavioral_tolerance == 'low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 10,
            'explanation': "Du kannst ein wenig Aktien in dein Portfolio aufnehmen."
        } 
    elif risk_ability == 'high' and risk_need == 'low' and behavioral_tolerance == 'moderate':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 20,
            'explanation': "Du kannst ein wenig Aktien in dein Portfolio aufnehmen."
        } 
    elif risk_ability == 'high' and risk_need == 'low' and behavioral_tolerance == 'moderate':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 30,
            'explanation': "Du hast nicht die Notwendigkeit eine höhere Aktienquote zu fahren."
        } 
    elif risk_ability == 'high' and risk_need == 'moderate' and behavioral_tolerance == 'very_low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 10,
            'explanation': "Aufgrund deiner Risikotoleranz bleibt deine Aktienquote recht niedrig."
        } 
    elif risk_ability == 'high' and risk_need == 'moderate' and behavioral_tolerance == 'low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 25,
            'explanation': "Aufgrund deiner Risikotoleranz bleibt deine Aktienquote recht niedrig."
        } 
    elif risk_ability == 'high' and risk_need == 'moderate' and behavioral_tolerance == 'moderate':
        return {
            'allocation': 'Mittel',
            'equity_percentage': 50,
            'explanation': ""
        } 
    elif risk_ability == 'high' and risk_need == 'moderate' and behavioral_tolerance == 'high':
        return {
            'allocation': 'Mittel',
            'equity_percentage': 60,
            'explanation': ""
        } 
    elif risk_ability == 'high' and (risk_need == 'high' or 'too high') and behavioral_tolerance == 'very_low':
        return {
            'allocation': 'Niedrig',
            'equity_percentage': 25,
            'explanation': "Überlege dich über Finanzen weiterzubilden um deine Risikotoleranz zu erhöhen. Du bist auf eine Aktienquote angewiesen um dein Ziel zu erreichen"
        } 
    elif risk_ability == 'high' and (risk_need == 'high' or 'too high') and behavioral_tolerance == 'low':
        return {
            'allocation': 'Mittel',
            'equity_percentage': 50,
            'explanation': "Überlege dich über Finanzen weiterzubilden um deine Risikotoleranz zu erhöhen. Du bist auf eine Aktienquote angewiesen um dein Ziel zu erreichen"
        }
    elif risk_ability == 'high' and (risk_need == 'high' or 'too high') and behavioral_tolerance == 'moderate':
        return {
            'allocation': 'Hoch',
            'equity_percentage': 75,
            'explanation': ""
        }
    elif risk_ability == 'high' and (risk_need == 'high' or 'too high') and behavioral_tolerance == 'high':
        return {
            'allocation': 'Hoch',
            'equity_percentage': 100,
            'explanation': "Du kannst voll ins Risiko gehen."
        }
    else:
        return {
            'allocation': 'Fehler',
            'equity_percentage': 0,
            'explanation': "Fehler bei Bestimmung deiner Aktienquote"
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
    additional_benefits = form_data.get('additional_benefits')
    risk_ability, risk_ability_text = determine_risk_ability(additional_benefits, monthly_savings, time_horizon)
    
    # Calculate behavioral tolerance
    behavioral_tolerance, behavioral_tolerance_text = determine_behavioral_tolerance(form_data.get('behavioral_answers', {}))
    
    # Determine portfolio allocation
    portfolio = determine_portfolio_allocation(risk_need, risk_ability, behavioral_tolerance)
    
    return {
        'required_equity_rate': required_equity_rate,
        'risk_need': risk_need,
        'risk_ability': risk_ability,
        'risk_ability_text': risk_ability_text,
        'behavioral_tolerance': behavioral_tolerance,
        'behavioral_tolerance_text': behavioral_tolerance_text,
        'allocation': portfolio['allocation'],
        'equity_percentage': portfolio['equity_percentage'],
        'explanation': portfolio['explanation']
    } 