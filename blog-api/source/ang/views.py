from django.shortcuts import render


def get_angular_template(request, path=None):
    template = 'ang/app/blog-list.html'
    context = {}
    return render(request, template, context)
