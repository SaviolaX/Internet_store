from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'product-comment-input',
                    'rows': 1, 'cols': 20
                }),
        }
