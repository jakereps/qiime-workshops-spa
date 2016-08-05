from django import forms


# TODO: add custom validation
class OrderForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email Address'})
    )

    def __init__(self, *args, **kwargs):
        workshop = kwargs.pop('workshop')
        super().__init__(*args, **kwargs)

        rate_set = workshop.rate_set.order_by('price')
        for rate in rate_set:
            self.fields[rate.name] = forms.IntegerField(min_value=0)
