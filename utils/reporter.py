from datetime import datetime

def generate_report(df, summary):

    hot_rows = ""
    warm_rows = ""
    cold_rows = ""

    for _, row in df.iterrows():
        if row["status"] == "Hot":
            color = "#e8f5e9"
            badge = "<span style='background:#2e7d32;color:white;padding:2px 10px;border-radius:20px;font-size:12px;'>🔥 Hot</span>"
        elif row["status"] == "Warm":
            color = "#fff8e1"
            badge = "<span style='background:#f57f17;color:white;padding:2px 10px;border-radius:20px;font-size:12px;'>Warm</span>"
        else:
            color = "#fce4ec"
            badge = "<span style='background:#b71c1c;color:white;padding:2px 10px;border-radius:20px;font-size:12px;'>❄️ Cold</span>"

        tr = f"""
        <tr style='background:{color}'>
            <td>{row['name']}</td>
            <td>{row['email']}</td>
            <td>{row['company']}</td>
            <td>{row['phone']}</td>
            <td>{row['score']}</td>
            <td>{row['score_reason']}</td>
            <td>{badge}</td>
        </tr>"""

        if row["status"] == "Hot":
            hot_rows += tr
        elif row["status"] == "Warm":
            warm_rows += tr
        else:
            cold_rows += tr

    all_rows = hot_rows + warm_rows + cold_rows

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lead Automation Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 40px;
                background: #f5f5f5;
                color: #333;
            }}
            h1 {{
                color: #1a237e;
            }}
            .date {{
                color: #888;
                font-size: 14px;
                margin-bottom: 30px;
            }}
            .cards {{
                display: flex;
                gap: 20px;
                margin-bottom: 40px;
            }}
            .card {{
                flex: 1;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                background: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }}
            .card h2 {{
                font-size: 36px;
                margin: 0;
            }}
            .card p {{
                margin: 6px 0 0;
                color: #666;
                font-size: 14px;
            }}
            .hot {{ border-top: 4px solid #2e7d32; }}
            .warm {{ border-top: 4px solid #f57f17; }}
            .cold {{ border-top: 4px solid #b71c1c; }}
            .total {{ border-top: 4px solid #1a237e; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }}
            th {{
                background: #1a237e;
                color: white;
                padding: 12px 16px;
                text-align: left;
                font-size: 14px;
            }}
            td {{
                padding: 12px 16px;
                font-size: 14px;
                border-bottom: 1px solid #eee;
            }}
        </style>
    </head>
    <body>
        <h1>📊 Marketing Automation Report</h1>
        <p class="date">Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>

        <div class="cards">
            <div class="card total">
                <h2>{summary['total']}</h2>
                <p>Total Leads</p>
            </div>
            <div class="card hot">
                <h2>{summary['hot']}</h2>
                <p>🔥 Hot Leads</p>
            </div>
            <div class="card warm">
                <h2>{summary['warm']}</h2>
                <p>Warm Leads</p>
            </div>
            <div class="card cold">
                <h2>{summary['cold']}</h2>
                <p>❄️ Cold Leads</p>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Company</th>
                    <th>Phone</th>
                    <th>Score</th>
                    <th>Score Reason</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {all_rows}
            </tbody>
        </table>
    </body>
    </html>
    """

    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report saved to {filename}")
    return filename