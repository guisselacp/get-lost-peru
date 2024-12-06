from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from blog.models import Post


@login_required
def userprofile(request):
    post_list = Post.objects.filter(author=request.user)

    return render(request, 'userprofile/userprofile.html', {
        'post_list': post_list,
    })
   