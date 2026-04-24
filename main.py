import pandas as pd
import schedule
import time
from utils.scorer import score_leads, get_summary
from utils.reporter import generate_report

# ── Core pipeline function ─────────────────────────
def run_pipeline():
    print("\n🚀 Starting Marketing Automation Pipeline...")
    print("─" * 45)

    # Step 1: Load data
    print("\n📂 Step 1: Loading leads...")
    df = pd.read_csv("data/leads.csv")
    print(f"   {len(df)} leads loaded.")

    # Step 2: Score leads
    print("\n🧠 Step 2: Scoring leads...")
    df = score_leads(df)
    print("   All leads scored.")

    # Step 3: Save scored data
    print("\n💾 Step 3: Saving scored data...")
    df.to_csv("data/scored_leads.csv", index=False)
    hot = df[df["status"] == "Hot"]
    warm = df[df["status"] == "Warm"]
    cold = df[df["status"] == "Cold"]
    hot.to_csv("data/hot_leads.csv", index=False)
    print("   Scored data saved to data/scored_leads.csv")
    print("   Hot leads saved to data/hot_leads.csv")

    # Step 4: Print summary
    summary = get_summary(df)
    print("\n📊 Step 4: Pipeline Summary")
    print("─" * 45)
    print(f"   Total leads  : {summary['total']}")
    print(f"   🔥 Hot       : {summary['hot']}")
    print(f"   Warm         : {summary['warm']}")
    print(f"   ❄️  Cold      : {summary['cold']}")
    print("─" * 45)

    # Step 5: Generate report
    print("\n📄 Step 5: Generating HTML report...")
    generate_report(df, summary)

    print("\n✅ Pipeline completed successfully!")
    print("─" * 45)

# ── Run once immediately ───────────────────────────
run_pipeline()

# ── Then schedule to run every day at 9am ─────────
print("\n⏰ Pipeline scheduled to run daily at 09:00 AM")
print("   Press Ctrl+C to stop.\n")
schedule.every().day.at("09:00").do(run_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)