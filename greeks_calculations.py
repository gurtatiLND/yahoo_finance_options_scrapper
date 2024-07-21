import math
from scipy.stats import norm

RISK_FREE_INTEREST = 0.0167  # Example risk-free rate

def calculate_delta(underlying_price, strike, days_left, implied_volatility, option_type):
    """Calculate Delta for European options."""
    if days_left <= 0 or implied_volatility <= 0:
        return 0
    
    d1 = (math.log(underlying_price / strike) + 
          (RISK_FREE_INTEREST + (implied_volatility ** 2) / 2) * (days_left / 365)) / \
         (implied_volatility * math.sqrt(days_left / 365))
    
    if option_type == 'calls':
        return norm.cdf(d1)
    elif option_type == 'puts':
        return norm.cdf(d1) - 1
    else:
        raise ValueError(f"Unknown option_type: {option_type}")

def calculate_gamma(underlying_price, strike, days_left, implied_volatility):
    """Calculate Gamma for European options."""
    if days_left <= 0 or implied_volatility <= 0:
        return 0
    
    d1 = (math.log(underlying_price / strike) + 
          (RISK_FREE_INTEREST + (implied_volatility ** 2) / 2) * (days_left / 365)) / \
         (implied_volatility * math.sqrt(days_left / 365))
    
    gamma = norm.pdf(d1) / (underlying_price * implied_volatility * math.sqrt(days_left / 365))
    return gamma

def calculate_rho(underlying_price, strike, days_left, implied_volatility, option_type):
    """Calculate Rho for European options."""
    if days_left <= 0 or implied_volatility <= 0:
        return 0
    
    d1 = (math.log(underlying_price / strike) + 
          (RISK_FREE_INTEREST + (implied_volatility ** 2) / 2) * (days_left / 365)) / \
         (implied_volatility * math.sqrt(days_left / 365))
    
    if option_type == 'calls':
        rho = strike * (days_left / 365) * norm.cdf(d1)
    elif option_type == 'puts':
        rho = -strike * (days_left / 365) * norm.cdf(-d1)
    else:
        raise ValueError(f"Unknown option_type: {option_type}")
    return rho

def calculate_theta(underlying_price, strike, days_left, implied_volatility, option_type):
    """Calculate Theta for European options."""
    if days_left <= 0 or implied_volatility <= 0:
        return 0
    
    d1 = (math.log(underlying_price / strike) + 
          (RISK_FREE_INTEREST + (implied_volatility ** 2) / 2) * (days_left / 365)) / \
         (implied_volatility * math.sqrt(days_left / 365))
    
    d2 = d1 - implied_volatility * math.sqrt(days_left / 365)
    
    if option_type == 'calls':
        theta = (-underlying_price * norm.pdf(d1) * implied_volatility / (2 * math.sqrt(days_left / 365)) - \
                 RISK_FREE_INTEREST * strike * math.exp(-RISK_FREE_INTEREST * (days_left / 365)) * norm.cdf(d2))
    elif option_type == 'puts':
        theta = (-underlying_price * norm.pdf(d1) * implied_volatility / (2 * math.sqrt(days_left / 365)) + \
                 RISK_FREE_INTEREST * strike * math.exp(-RISK_FREE_INTEREST * (days_left / 365)) * norm.cdf(-d2))
    else:
        raise ValueError(f"Unknown option_type: {option_type}")
    return theta

def calculate_vega(underlying_price, strike, days_left, implied_volatility):
    """Calculate Vega for European options."""
    if days_left <= 0 or implied_volatility <= 0:
        return 0
    
    d1 = (math.log(underlying_price / strike) + 
          (RISK_FREE_INTEREST + (implied_volatility ** 2) / 2) * (days_left / 365)) / \
         (implied_volatility * math.sqrt(days_left / 365))
    
    vega = underlying_price * norm.pdf(d1) * math.sqrt(days_left / 365)
    return vega
