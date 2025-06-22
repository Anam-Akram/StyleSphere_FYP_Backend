from django.urls import path, include, re_path
from django.views.generic import TemplateView

from User.views import *

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.social.urls')),
    path('tailor_data/', get_tailor_data, name='get_tailor_data'),
    path('get_tailors_data/', get_tailors_data, name='get_tailors_data')
]

# urlpatterns += [re_path(r'^.*',
#                         TemplateView.as_view(template_name="index.html"))]
