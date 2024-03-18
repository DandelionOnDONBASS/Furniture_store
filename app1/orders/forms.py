import re
from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=(("1", "True"), ("0", "False")))
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=(("1", "True"), ("0", "False")),
    )



    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("Телефон должен содержать только цифры")
        
        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат телефона")
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        requires_delivery = cleaned_data.get("requires_delivery")
        delivery_address = cleaned_data.get("delivery_address")

        if requires_delivery == "1" and not delivery_address:
            self.add_error("delivery_address", "Укажите адрес доставки")
      
        return cleaned_data
        