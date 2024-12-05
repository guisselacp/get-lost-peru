from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from blog.models import Post

# Create your views here.
@login_required
def userprofile(request):
    posts = Post.objects.filter(author=request.user)

    return render(request, 'userprofile/userprofile.html',)
   