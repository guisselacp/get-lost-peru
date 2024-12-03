from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """ Form to create a post """
    
    class Meta:
        model = Post
        fields = ['title', 'featured_image', 'excerpt', 'content']

        #contents = forms.CharField(widget=RichTextWidget())

        widget = {
            "excerpt": forms.Textarea(attrs={"rows": 5}),
        }

        labels = {
            "title": "Post Title",
            "featured_image": "Post Image",
            "excerpt": "Excerpt",
            "content": "Content",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)