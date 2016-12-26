from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.shortcuts import render

import os


class AngularTemplateView(View):

    def get(self, request, item=None, *args, **kwargs):
        template_dir_path = settings.TEMPLATES[0]['DIRS'][0]
        final_path = os.path.join(template_dir_path, 'ang', 'app', item + '.html')
        try:
            html = open(final_path)
            return HttpResponse(html)
        except:
            raise Http404

# def get_angular_template(request, item=None):
#     template = 'ang/app/blog-list.html'
#     context = {}
#     print(item)
#     return render(request, template, context)
