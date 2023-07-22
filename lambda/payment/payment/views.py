from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView


def success(request):
     return render(request,'success.html')

class HomePageView(TemplateView):
     template_name = 'home.html'
     def get_context_data(self, **kwargs): # new
          context =super().get_context_data(**kwargs)
          context['key'] = settings.PUBLISHABLE_KEY
          return context