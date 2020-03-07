from django.shortcuts import render


def home(request):
    template_name = 'ideas/base.html'
    return render(request, template_name)
