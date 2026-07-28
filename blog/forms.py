from django import forms

from .models import Blog, Comment


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog

        fields = [
            "title",
            "category",
            "tags",
            "featured_image",
            "content",
            "status",
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 8
                }
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = [
            "content",
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your comment here...",
                }
            ),
        }

        labels = {
            "content": "",
        }