from django import forms


class LinkForm(forms.Form):
	url = forms.URLField(max_length=256, label='', widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': "Введите ссылку",
		'aria-describedby': "basic-addon2",
	}))
