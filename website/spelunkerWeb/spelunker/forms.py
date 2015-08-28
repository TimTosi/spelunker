from django import forms

class SearchForm(forms.Form):
	refferer = forms.CharField(widget=forms.HiddenInput())
	search = forms.CharField(label=False, max_length=70, widget=forms.TextInput(attrs={'class': 'special mdl-color--white mdl-cell mdl-cell--10-col search'}))