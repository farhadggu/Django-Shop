#==>Library Import
from django import forms
#==>Local Import
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'rows': '3', 'placeholder': 'متن پاسخ', 'class':'form-control'})