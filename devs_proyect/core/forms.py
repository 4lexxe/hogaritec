from django import forms
from sale.models import Customer
from django.core.exceptions import ValidationError

class EditCustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'avatar']
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number and len(phone_number) < 4:
            raise ValidationError("El número de teléfono debe tener al menos 4 dígitos.")
        
        if phone_number and not phone_number.isdigit():
            raise ValidationError("El número de teléfono debe contener solo números.")

        return phone_number
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Eliminar la imagen si el checkbox está marcado
        if self.cleaned_data.get('delete_avatar'):
            instance.avatar.delete(save=False)
            instance.avatar = None
        if commit:
            instance.save()
        return instance
