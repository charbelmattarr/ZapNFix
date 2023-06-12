from django import forms
from django.core.exceptions import ValidationError
from .models import Repair

class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['desc', 'status', 'repairDate','isDelivery','pricing','notes']

    def clean(self):
        cleaned_data = super().clean()

        desc = cleaned_data.get('desc')
        if not desc:
            self.add_error('desc', "Description is required.")

        status = cleaned_data.get('status')
        if not status:
            self.add_error('status', "Status is required.")

        repair_date = cleaned_data.get('repairDate')
        if repair_date and cleaned_data.get('createdDate') and repair_date <= cleaned_data.get('createdDate'):
            self.add_error('repairDate', "Repair date should be in the future.")

        pricing = cleaned_data.get('pricing')
        if pricing is not None and pricing < 0:
            self.add_error('pricing', "Pricing should be a positive value.")

        feedback_rate = cleaned_data.get('feedbackRate')
        if feedback_rate is not None and (feedback_rate < 0 or feedback_rate > 5):
            self.add_error('feedbackRate', "Feedback rate should be between 0 and 5.")





        return cleaned_data
