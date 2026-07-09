import pandas as pd
from datetime import datetime

def decay_multiplier(date_str, half_life_days=30):
    """Recent actions score higher. Score halves every 30 days."""
    if not date_str or pd.isna(date_str):
        return 0
    action_date = datetime.strptime(str(date_str), "%Y-%m-%d")
    days_ago = (datetime.now() - action_date).days
    return max(0.1, 0.5 ** (days_ago / half_life_days))

def score_leads(df):
    def score_lead(row):
        score = 0
        # Base weights: form fill is strongest signal
        if row["filled_form"]:
            score += 50 * decay_multiplier(row.get("filled_form_date"))
        if row["visited_site"]:
            score += 35 * decay_multiplier(row.get("visited_site_date"))
        if row["opened_email"]:
            score += 15 * decay_multiplier(row.get("opened_email_date"))

        # Compound bonus: multiple actions = more intent
        actions = sum([row["opened_email"], row["visited_site"], row["filled_form"]])
        if actions == 3:
            score *= 1.2
        elif actions == 2:
            score *= 1.1

        return round(min(score, 100), 1)  # cap at 100

    def score_reason(row):
        reasons = []
        if row["filled_form"]:
            reasons.append("Filled form")
        if row["visited_site"]:
            reasons.append("Visited site")
        if row["opened_email"]:
            reasons.append("Opened email")
        return " · ".join(reasons) if reasons else "No activity"

    def label_lead(score):
        if score >= 70:
            return "Hot"
        elif score >= 35:
            return "Warm"
        else:
            return "Cold"

    df["score"] = df.apply(score_lead, axis=1)
    df["score_reason"] = df.apply(score_reason, axis=1)
    df["status"] = df["score"].apply(label_lead)
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    return df

def get_summary(df):
    return {
        "total": len(df),
        "hot": len(df[df["status"] == "Hot"]),
        "warm": len(df[df["status"] == "Warm"]),
        "cold": len(df[df["status"] == "Cold"]),
        "avg_score": round(df["score"].mean(), 1),
    }