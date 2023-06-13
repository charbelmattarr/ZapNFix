from django import forms
from django.core.exceptions import ValidationError
from .models import Repair, User
# forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RepairForm(forms.ModelForm):
    # user_idClient = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    # user_idTech = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    cleaned_data = None
    class Meta:
        model = Repair
        fields = ['desc', 'status', 'repairDate','isDelivery','pricing','notes','user_idTech']

    def clean(self):
        cleaned_data = super().clean()
        user_idTech_id = cleaned_data.get('user_idTech')

        if user_idTech_id:
            try:
                user_idTech = User.objects.get(username=user_idTech_id)
                cleaned_data['user_idTech'] = user_idTech
            except User.DoesNotExist:
                self.add_error('user_idTech', "Invalid User ID")

        return cleaned_data
    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data is None:
    #         cleaned_data = {}
    #     desc = cleaned_data.get('desc')
    #     if not desc:
    #         self.add_error('desc', "Description is required.")
    #
    #     status = cleaned_data.get('status')
    #     if not status:
    #         self.add_error('status', "Status is required.")
    #
    #     repair_date = cleaned_data.get('repairDate')
    #     created_date = cleaned_data.get('createdDate')
    #     if repair_date and created_date and repair_date <= created_date:
    #         self.add_error('repairDate', "Repair date should be in the future.")
    #
    #     pricing = cleaned_data.get('pricing')
    #     if pricing is not None and pricing < 0:
    #         self.add_error('pricing', "Pricing should be a positive value.")
    #
    #     feedback_rate = cleaned_data.get('feedbackRate')
    #     if feedback_rate is not None and (feedback_rate < 0 or feedback_rate > 5):
    #         self.add_error('feedbackRate', "Feedback rate should be between 0 and 5.")
    #
    #     self.cleaned_data = cleaned_data  # Assign the cleaned data to the attribute
    #
    #     return cleaned_data

    # def save(self, commit=True):
    #         repair = super().save(commit=False)
    #         print("before retrieve ")
    #         # Retrieve the selected user objects based on the dropdown choices
    #         client_username = self.cleaned_data['user_idClient']
    #
    #         print("before retrieve ")
    #         technician_username = self.cleaned_data['user_idTech']
    #         # Get the User instances based on the selected client_username and technician_username
    #         client_user = User.objects.get_object_or_404(username=client_username)
    #         technician_user = User.objects.get_object_or_404(username=technician_username)
    #
    #         repair.user_idClient = client_user
    #         repair.user_idTech = technician_user
    #
    #
    #
    #         if commit:
    #             repair.save()
    #
    #         return repair





class RegistrationForm(UserCreationForm):
        class Meta:
                model = User
                fields = ['email', 'username', 'role', 'number', 'location', 'first_name', 'last_name']

        def clean(self):
                cleaned_data = super().clean()
                email = cleaned_data.get('email')
                username = cleaned_data.get('username')

                if User.objects.filter(email=email).exists():
                        self.add_error('email', 'This email is already taken. Please choose a different one.')

                if User.objects.filter(username=username).exists():
                        self.add_error('username', 'This username is already taken. Please choose a different one.')

                return cleaned_data

# class RepairForm(forms.ModelForm):
#
#         class Meta:
#             model = Repair
#             fields = ['image']