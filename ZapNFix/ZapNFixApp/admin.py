from django.contrib import admin
from django import forms
from .models import Repair, User, Type, Brand, Component, Problem




class ProblemForm(forms.ModelForm):
    type_desc = forms.ModelChoiceField(queryset=Type.objects.all(), empty_label=None, to_field_name='desc',
                                       label='Type')
    component_desc = forms.ModelChoiceField(queryset=Component.objects.all(), empty_label=None, to_field_name='desc',
                                            label='Component')

    class Meta:
        model = Problem
        fields = ['desc', 'type_desc', 'component_desc']

    def save(self, commit=True):
        problem = super().save(commit=False)
        type_desc = self.cleaned_data['type_desc']
        component_desc = self.cleaned_data['component_desc']
        # Create or get the Type and Component instances based on the selected type_desc and component_desc
        type_instance, _ = Type.objects.get_or_create(desc=type_desc)
        component_instance, _ = Component.objects.get_or_create(desc=component_desc)
        problem.type_id = type_instance
        problem.component_id = component_instance
        if commit:
            problem.save()
        return problem


class ProblemAdmin(admin.ModelAdmin):
    form = ProblemForm
    search_fields = ['desc', 'type_desc', 'component_desc']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'role', 'number', 'location', 'is_active', 'is_staff', 'is_superuser',
                  'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    search_fields = ['email', 'username', 'role', 'number', 'location', 'is_active', 'is_staff', 'is_superuser',
                  'first_name', 'last_name']


class RepairForm(forms.ModelForm):

    user_idClient = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    user_idTech = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    class Meta:
        model = Repair
        fields = ['desc', 'status', 'repairDate', 'user_idClient', 'user_idTech']

        search_fields = ['desc', 'status', 'repairDate', 'user_idClient', 'user_idTech']
    # def save(self, commit=True):
    #     repair = super().save(commit=False)
    #     client_username = self.cleaned_data['user_idClient']
    #     technician_username = self.cleaned_data['user_idTech']
    #     # Get the User instances based on the selected client_username and technician_username
    #     client_user = User.objects.get(username=client_username)
    #     technician_user = User.objects.get(username=technician_username)
    #     # Assign the selected User instances to the user_idClient and user_idTech fields
    #     repair.user_idClient = client_user
    #     repair.user_idTech = technician_user
    #     if commit:
    #         repair.save()
    #     return repair
    #

class RepairAdmin(admin.ModelAdmin):
    form = RepairForm
    search_fields = ['desc', 'status', 'repairDate', 'client_username', 'technician_username']

##############################################
class BrandForm(forms.ModelForm):
    type_desc = forms.ModelChoiceField(queryset=Type.objects.all(), empty_label=None, to_field_name='desc',
                                       label='Type')

    class Meta:
        model = Brand
        fields = ['desc', 'type_desc']

    def save(self, commit=True):
        brand = super().save(commit=False)
        type_desc = self.cleaned_data['type_desc']
        # Create or get the Type instance based on the selected type_desc
        type_instance, _ = Type.objects.get_or_create(desc=type_desc)
        brand.type_id = type_instance
        if commit:
            brand.save()
        return brand

class BrandAdmin(admin.ModelAdmin):
    form = BrandForm
    search_fields = ['desc']

class TypeAdmin(admin.ModelAdmin):
    search_fields = ['desc']
class ComponentAdmin(admin.ModelAdmin):
    search_fields = ['desc']

admin.site.register(Repair, RepairAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Type,TypeAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Brand, BrandAdmin)
