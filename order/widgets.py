from django import forms


class CustomSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        self.data = kwargs.pop('data', {})
        super().__init__(*args, **kwargs)

    def create_option(self, name, value, *args, **kwargs):
        options = super().create_option(name, value, *args, **kwargs)
        for k, v in self.data.items():
            options['attrs'][k] = v[options['value']]
        return options
