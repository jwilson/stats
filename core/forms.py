from django import forms


class TableSortForm(forms.Form):
    longest_gains = forms.IntegerField()
    touchdowns = forms.IntegerField()
    yards = forms.IntegerField()
