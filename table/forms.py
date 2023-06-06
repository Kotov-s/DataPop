from django import forms

class FileForm(forms.Form):
    text = forms.CharField(label="Название треда", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    check = forms.BooleanField(label="Показывать объяснения", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input mx-auto'}))
    public = forms.BooleanField(label="Сделать публичным", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input mx-auto'}))

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError('Это поле требуется')
        if len(text) < 5:
            raise forms.ValidationError('Название треда должно быть как минимум в 5 символов')
        return text
    