from django import forms

class CompanyTicker(forms.Form):
    ticker = forms.CharField(help_text="Enter company ticker.")

    def clean_company_ticker(self):
        data = self.cleaned_data['ticker']

        # Check if a date is not in the past.
        if not data:
            raise ValidationError(_('Invalid ticker - cannot be null'))

        # Remember to always return the cleaned data.
        return data