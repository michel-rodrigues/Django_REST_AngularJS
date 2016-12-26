from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post


class PostForm(forms.ModelForm):

    # implemeta botões para formatação através de markdown
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    # implementa um widget para selecionar a data com botões dropdown
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'draft',
            'publish',
        ]
