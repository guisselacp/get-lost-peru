from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.views.generic import CreateView
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Post, Comment
from .forms import PostForm, CommentForm, EditPostForm

from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin
)

# Create your views here.

class AddPost(LoginRequiredMixin, CreateView):
    """
    A model to create a post
    """
    template_name = 'blog/blog_create.html'
    model = Post
    form_class = PostForm
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.author = self.request.user

        # save the post instance
        response = super().form_valid(form)

        # check if the post is approved or awaiting approval
        if self.object.status == 0:
            messages.info(
                self.request, 'Post submitted and awaiting approval!')

        return response

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    # Here send the comment info - POST
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval!'
            )

    comment_form = CommentForm()

    # context = {"post": post}
    return render(request, "blog/post_detail.html", 
        {
            "post":post,
            "comments":comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            'liked': liked,
        },
    )


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class PostLike(View):
    """
    A model to like/unlike the post
    """
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
       
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


@login_required
def edit(request, pk): 
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post successfully edited!")
            return redirect('post_detail.html', pk=post.pk)
    else:
        form = EditPostForm(instance=post)

    return render(request, 'blog/blog_create.html', {
        'form': form,
        'title': 'Edit post',
    })

@login_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
       post.delete()
       messages.success(request, "Post successfully deleted!")
       return redirect('userprofile:userprofile')
    return render( request,'delete.html', {
        'post':post
    })
