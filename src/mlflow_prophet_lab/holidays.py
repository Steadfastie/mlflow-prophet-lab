import holidays
import pandas as pd

def get_holidays(years: list[int]) -> pd.DataFrame:
    country_codes = ["US", "FR", "DE", "IT", "ES"]
    all_holidays = []
    
    for code in country_codes:
        for dt, name in holidays.country_holidays(code, years=years).items():
            all_holidays.append({"ds": pd.to_datetime(dt), "holiday": f"{code}_{name}"})
    
    return pd.DataFrame(all_holidays)