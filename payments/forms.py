import functools

from django import forms


class OrderForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Order Email Address'})
    )

    def __init__(self, *args, **kwargs):
        workshop = kwargs.pop('workshop')
        super().__init__(*args, **kwargs)

        self.rate_set = workshop.rate_set.order_by('price')
        for rate in self.rate_set:
            self.fields[rate.name] = forms.IntegerField(initial=0, min_value=0)

    def clean(self):
        cleaned_data = super().clean()
        rates = {}
        for rate in self.rate_set:
            rates[rate.name] = cleaned_data[rate.name]

        if not functools.reduce(lambda x, y: x + y, rates.values()):
            raise forms.ValidationError('Order can not be empty.')

        return cleaned_data


class OrderDetailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Ticketholder\'s Email'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ticketholder\'s Name'})
    )
    rate = forms.CharField(widget=forms.HiddenInput())
