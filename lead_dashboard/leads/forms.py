from django import forms


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload leads CSV",
        help_text="Columns required: name, email, company, job_title, phone, "
                   "opened_email, visited_site, filled_form, opened_email_date, "
                   "visited_site_date, filled_form_date",
    )

    def clean_csv_file(self):
        file = self.cleaned_data["csv_file"]
        if not file.name.endswith(".csv"):
            raise forms.ValidationError("Please upload a .csv file.")
        return file
