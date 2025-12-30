from prophet.diagnostics import cross_validation

def run_cross_validation(model):
    """
    Run Prophet cross-validation.
    """
    cv_results = cross_validation(
        model,
        parallel="processes",
        initial="7300 days",   # ~20 years
        period="180 days",
        horizon="365 days"
    )  # ~12 points

    return cv_results