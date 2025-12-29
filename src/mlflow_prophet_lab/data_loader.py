import csv
from pathlib import Path
from attr import dataclass
import psycopg
from datetime import date, datetime

from .config import AppConfig

@dataclass
class RateRecord:
    date: date
    rate: float

def seed_data(config: AppConfig) -> None:
    """
    Loads exchange rates data from CSV file in dataseed folder into PostgreSQL database.
    
    The CSV file is expected to have columns containing 'date' and 'us dollar/euro' (case insensitive).
    """
    print("seeding data into database...")

    root = Path(__file__).resolve().parents[2]
    csv_path = root / config.dataseed_path
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    with psycopg.connect(config.db_uri) as conn:
        with conn.cursor() as cur:
    
            cur.execute("""
                CREATE TABLE IF NOT EXISTS exchange_rates (
                    date DATE PRIMARY KEY,
                    rate DECIMAL(10,4)
                )
            """)
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                fieldnames = reader.fieldnames
                if fieldnames is None:
                    raise ValueError("CSV file has no header row.")
                
                date_col = next(name for name in fieldnames if 'date' in name.lower())
                rate_col = next(name for name in fieldnames if 'us dollar/euro' in name.lower())
                
                data: list[tuple[date, float]] = []
                for row in reader:
                    date_str = row[date_col]
                    rate_str = row[rate_col]

                    if not rate_str or not rate_str.strip():
                        continue 

                    data.append((datetime.strptime(date_str, "%Y-%m-%d").date(), float(rate_str)))

                cur.executemany(
                    query="""
                    INSERT INTO exchange_rates (date, rate)
                    VALUES (%s, %s)
                    ON CONFLICT (date) DO NOTHING
                    """,
                    params_seq=data
                )

                conn.commit()

    print("data seeding completed")

def load_data(config: AppConfig) -> list[RateRecord]:
    """
    Loads exchange rates data from PostgreSQL database into a list of RateRecord.
    """
    records: list[RateRecord] = []
    with psycopg.connect(config.db_uri) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT date, rate FROM exchange_rates ORDER BY date ASC")
            rows = cur.fetchall()

            records = [RateRecord(
                date=row[0], 
                rate=float(row[1])) 
                for row in rows]

    return records

