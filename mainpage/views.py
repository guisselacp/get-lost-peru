from django.views.generic import TemplateView

class Mainpage(TemplateView):
    template_name = "mainpage/mainpage.html"
