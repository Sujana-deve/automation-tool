import pandas as pd

def score_leads(df):
    def score_lead(row):
        score = 0
        if row["opened_email"] == True:
            score += 30
        if row["visited_site"] == True:
            score += 40
        if row["filled_form"] == True:
            score += 30
        return score

    def label_lead(score):
        if score >= 70:
            return "Hot"
        elif score >= 40:
            return "Warm"
        else:
            return "Cold"

    df["score"] = df.apply(score_lead, axis=1)
    df["status"] = df["score"].apply(label_lead)
    return df

def get_summary(df):
    summary = {
        "total": len(df),
        "hot": len(df[df["status"] == "Hot"]),
        "warm": len(df[df["status"] == "Warm"]),
        "cold": len(df[df["status"] == "Cold"]),
    }
    return summary