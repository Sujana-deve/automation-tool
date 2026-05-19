import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_leads(n=100):
    leads = []
    now = datetime.now()

    for _ in range(n):
        # Randomize action timestamps (0–90 days ago)
        opened_date = now - timedelta(days=random.randint(0, 90)) if random.random() > 0.3 else None
        visited_date = now - timedelta(days=random.randint(0, 60)) if random.random() > 0.4 else None
        filled_date = now - timedelta(days=random.randint(0, 30)) if random.random() > 0.7 else None

        leads.append({
            "name": fake.name(),
            "email": fake.email(),
            "company": fake.company(),
            "job_title": fake.job(),
            "phone": fake.phone_number(),
            "opened_email": opened_date is not None,
            "visited_site": visited_date is not None,
            "filled_form": filled_date is not None,
            "opened_email_date": opened_date.strftime("%Y-%m-%d") if opened_date else None,
            "visited_site_date": visited_date.strftime("%Y-%m-%d") if visited_date else None,
            "filled_form_date": filled_date.strftime("%Y-%m-%d") if filled_date else None,
        })

    return pd.DataFrame(leads)

if __name__ == "__main__":
    df = generate_leads(200)
    df.to_csv("data/leads.csv", index=False)
    print(f"Generated {len(df)} leads → data/leads.csv")
    print(df[["name", "opened_email", "visited_site", "filled_form"]].head())