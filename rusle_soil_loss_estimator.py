import math

def compute_ls_factor(slope_length_m, slope_steepness_percent):
    """
    Compute LS factor from slope length (m) and slope steepness (%).
    LS = (λ/22.13)^m * (65.41 sin²θ + 4.56 sinθ + 0.065)
    where m depends on slope steepness.
    """
    if slope_length_m <= 0 or slope_steepness_percent < 0:
        raise ValueError("Slope length must be positive and steepness non-negative.")
    
    theta_rad = math.atan(slope_steepness_percent / 100.0)
    sin_theta = math.sin(theta_rad)
    sin2_theta = sin_theta ** 2
    
    # Determine m factor
    if slope_steepness_percent >= 5:
        m = 0.5
    elif slope_steepness_percent >= 3:
        m = 0.4
    elif slope_steepness_percent >= 1:
        m = 0.3
    else:
        m = 0.2
    
    # Slope length ratio
    length_ratio = slope_length_m / 22.13
    # Slope steepness factor
    steepness_factor = 65.41 * sin2_theta + 4.56 * sin_theta + 0.065
    ls = (length_ratio ** m) * steepness_factor
    return ls

def compute_annual_soil_loss(R, K, LS, C, P):
    """A = R × K × LS × C × P. Returns annual soil loss in t/ha/yr."""
    return R * K * LS * C * P
