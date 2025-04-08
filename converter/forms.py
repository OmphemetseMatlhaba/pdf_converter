from django import forms

class PDFUploadForm(forms.Form):
    
    files = forms.FileField(
           widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(PDFUploadForm, self).__init__(*args, **kwargs)
        self.fields['files'].widget = forms.FileInput(attrs={'multiple': False})
