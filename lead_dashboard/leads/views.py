import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import CSVUploadForm
from .models import UploadBatch, Lead
from .scoring import score_leads, get_summary

REQUIRED_COLUMNS = [
    "name", "email", "opened_email", "visited_site", "filled_form",
]


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]

            try:
                df = pd.read_csv(csv_file)
            except Exception as e:
                messages.error(request, f"Couldn't read that CSV: {e}")
                return render(request, "leads/upload.html", {"form": form})

            missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
            if missing:
                messages.error(
                    request,
                    f"CSV is missing required column(s): {', '.join(missing)}",
                )
                return render(request, "leads/upload.html", {"form": form})

            # Boolean columns may arrive as strings ("True"/"False") from CSV
            for col in ["opened_email", "visited_site", "filled_form"]:
                df[col] = df[col].astype(str).str.strip().str.lower().map(
                    {"true": True, "1": True, "false": False, "0": False, "nan": False}
                ).fillna(False)

            df = score_leads(df)
            summary = get_summary(df)

            batch = UploadBatch.objects.create(filename=csv_file.name)

            leads_to_create = []
            for _, row in df.iterrows():
                leads_to_create.append(Lead(
                    batch=batch,
                    name=row.get("name", ""),
                    email=row.get("email", ""),
                    company=row.get("company", "") or "",
                    job_title=row.get("job_title", "") or "",
                    phone=str(row.get("phone", "") or ""),
                    opened_email=bool(row.get("opened_email", False)),
                    visited_site=bool(row.get("visited_site", False)),
                    filled_form=bool(row.get("filled_form", False)),
                    opened_email_date=pd.to_datetime(row.get("opened_email_date"), errors="coerce").date() if pd.notna(row.get("opened_email_date")) else None,
                    visited_site_date=pd.to_datetime(row.get("visited_site_date"), errors="coerce").date() if pd.notna(row.get("visited_site_date")) else None,
                    filled_form_date=pd.to_datetime(row.get("filled_form_date"), errors="coerce").date() if pd.notna(row.get("filled_form_date")) else None,
                    score=row["score"],
                    score_reason=row["score_reason"],
                    status=row["status"],
                ))
            Lead.objects.bulk_create(leads_to_create)

            messages.success(
                request,
                f"Scored {summary['total']} leads — {summary['hot']} hot, "
                f"{summary['warm']} warm, {summary['cold']} cold.",
            )
            return redirect("dashboard", batch_id=batch.id)
    else:
        form = CSVUploadForm()

    recent_batches = UploadBatch.objects.order_by("-uploaded_at")[:5]
    return render(request, "leads/upload.html", {"form": form, "recent_batches": recent_batches})


def dashboard(request, batch_id=None):
    if batch_id:
        batch = get_object_or_404(UploadBatch, id=batch_id)
    else:
        batch = UploadBatch.objects.order_by("-uploaded_at").first()

    if not batch:
        return redirect("upload_csv")

    leads = batch.leads.all()
    status_filter = request.GET.get("status")
    if status_filter in ("Hot", "Warm", "Cold"):
        leads = leads.filter(status=status_filter)

    summary = {
        "total": batch.leads.count(),
        "hot": batch.leads.filter(status="Hot").count(),
        "warm": batch.leads.filter(status="Warm").count(),
        "cold": batch.leads.filter(status="Cold").count(),
        "avg_score": round(
            sum(l.score for l in batch.leads.all()) / batch.leads.count(), 1
        ) if batch.leads.count() else 0,
    }

    return render(request, "leads/dashboard.html", {
        "batch": batch,
        "leads": leads,
        "summary": summary,
        "status_filter": status_filter,
    })
