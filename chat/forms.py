from django import forms

class FileForm(forms.Form):
    file = forms.FileField(label="CSV файл", widget=forms.ClearableFileInput(attrs={'accept': '.csv', 'class': 'form-control'}))
    text = forms.CharField(label="Название треда", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    check = forms.BooleanField(label="Показывать объяснения", required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input mx-auto'}))
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 20 * 8 * 1024 * 1024:
                raise forms.ValidationError('Файл должен быть меньше 20mb.')
            if not file.name.endswith('.csv'):
                raise forms.ValidationError('Можно загружать только CSV файлы.')
        return file
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError('Это поле требуется')
        if len(text) < 5:
            raise forms.ValidationError('Название треда должно быть как минимум в 5 символов')
        return text