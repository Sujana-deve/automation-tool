import pandas as pd
import schedule
import time
import logging
from datetime import datetime
from data_generator import generate_leads
from utils.scorer import score_leads, get_summary
from utils.reporter import generate_report

# ── Logging setup ──────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ── Core pipeline function ─────────────────────────
def run_pipeline():
    log.info("Starting pipeline...")
    print("─" * 45)

    try:
        # Step 1: Generate + load data
        print("\n📂 Step 1: Generating & loading leads...")
        generate_leads(200)          # ← moved inside so scheduler gets fresh data
        df = pd.read_csv("data/leads.csv")
        print(f"   {len(df)} leads loaded.")

        # Step 2: Score leads
        print("\n🧠 Step 2: Scoring leads...")
        df = score_leads(df)
        print("   All leads scored.")

        # Step 3: Save scored data
        print("\n💾 Step 3: Saving scored data...")
        df.to_csv("data/scored_leads.csv", index=False)
        hot  = df[df["status"] == "Hot"]
        warm = df[df["status"] == "Warm"]
        cold = df[df["status"] == "Cold"]
        hot.to_csv("data/hot_leads.csv", index=False)
        warm.to_csv("data/warm_leads.csv", index=False)
        cold.to_csv("data/cold_leads.csv", index=False)
        print("   Scored data saved.")

        # Step 4: Summary
        summary = get_summary(df)
        print("\n📊 Step 4: Pipeline Summary")
        print("─" * 45)
        print(f"   Total leads  : {summary['total']}")
        print(f"   🔥 Hot        : {summary['hot']}")
        print(f"   🌤  Warm       : {summary['warm']}")
        print(f"   ❄️  Cold       : {summary['cold']}")
        print(f"   📈 Avg score  : {summary['avg_score']}")
        print("─" * 45)

        # Step 5: Report
        print("\n📄 Step 5: Generating HTML report...")
        generate_report(df, summary)

        log.info("Pipeline completed successfully.")
        print("\n✅ Pipeline completed successfully!")

    except Exception as e:
        log.error(f"Pipeline failed: {e}")
        print(f"\n❌ Pipeline failed: {e}")
        # scheduler keeps running even if this run crashed

    print("─" * 45)

# ── Run once immediately ───────────────────────────
run_pipeline()

# ── Schedule daily at 9am ─────────────────────────
print("\n⏰ Pipeline scheduled to run daily at 09:00 AM")
print("   Press Ctrl+C to stop.\n")
schedule.every().day.at("09:00").do(run_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)