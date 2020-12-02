from django import forms
class ImageUploadForm(forms.Form):
    OPTIONS = (
        ('DCP','Dark Channel'),
        ('RawT','Raw Transmission'),
        ('RefineT','Refine Transmission'),
        ('PImg', 'Pre Processes Image'),
        ('FImg','Final Image')
    )
    img = forms.ImageField(label = False)
    imgShow = forms.MultipleChoiceField(label = False, widget = forms.CheckboxSelectMultiple(attrs= {
        'class': 'text-white'
    }), choices = OPTIONS)
    