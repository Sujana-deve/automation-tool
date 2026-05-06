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

    def score_reason(row):
        reasons = []
        if row["opened_email"] == True:
            reasons.append("Opened email")
        if row["visited_site"] == True:
            reasons.append("Visited site")
        if row["filled_form"] == True:
            reasons.append("Filled form")
        return " · ".join(reasons) if reasons else "No activity"

    def label_lead(score):
        if score >= 70:
            return "Hot"
        elif score >= 40:
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
    }