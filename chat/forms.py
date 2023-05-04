from django import forms

class FileForm(forms.Form):
    file = forms.FileField(label="CSV file", widget=forms.ClearableFileInput(attrs={'accept': '.csv'}))
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 20 * 1024 * 1024:
                raise forms.ValidationError('File size must be no more than 20mb.')
            if not file.name.endswith('.csv'):
                raise forms.ValidationError('Only CSV files are allowed.')
        return file