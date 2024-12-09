from django.shortcuts import render
from django.contrib import messages
from .models import About
from .forms import DropForm

# Create your views here.
def about_me(request):
    """
    Render the most recent information on the website author and allows user drop a line.
    Display an individual instance of: model:`about.About`.
    **Context**
    ``about``
        The most recent instance of :model:`about.About`.
    ``drop_form``
        An instance of :form:`about.DropForm`.
    **Template:**
    :template:`about/about.html`     
    """
    if request.method == "POST":
        drop_form = DropForm(data=request.POST)
        if drop_form.is_valid():
            drop_form.save()
            messages.add_message(request, messages.SUCCESS, "Message request received! I endeavour to respond within 3 working days.")

    about = About.objects.all().order_by('-updated_on').first()
    drop_form = DropForm()

    return render(request, "about/about.html", 
        {
            "about": about,
            "drop_form": drop_form
        },
    )