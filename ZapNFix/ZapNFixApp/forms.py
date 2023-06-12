from django import forms
from django.core.exceptions import ValidationError
from .models import Repair, User


class RepairForm(forms.ModelForm):

    class Meta:
        model = Repair
        fields = ['desc', 'status', 'repairDate','isDelivery','pricing','notes', 'user_idTech', 'user_idClient']

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
    def save(self, commit=True):
            repair = super().save(commit=False)
            print("before retrieve ")
            # Retrieve the selected user objects based on the dropdown choices
            client_username = self.cleaned_data['user_idClient']

            print("before retrieve ")
            technician_username = self.cleaned_data['user_idTech']
            # Get the User instances based on the selected client_username and technician_username
            client_user = User.objects.get(username=client_username)
            technician_user = User.objects.get(username=technician_username)

            repair.user_idClient = client_user
            repair.user_idTech = technician_user


            if commit:
                repair.save()

            return repair


