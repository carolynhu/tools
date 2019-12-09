from django import forms
from . import download
cur_release_names, master_release_names = download.download_benchmark_csv()

CHOICES = cur_release_names
print("#####")
print(CHOICES)


class ReleaseForm(forms.Form):
    # release_name = forms.ChoiceField(choices=CHOICES)
    release_name = forms.CharField(widget=forms.Select)
