from django.urls import path, include
from django.views.generic.base import RedirectView

from django.contrib import admin

admin.autodiscover()

#import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("",RedirectView.as_view(url="amtrak/"), name='go-to-amtrak'),
    path("admin/", admin.site.urls),
    path('amtrak/', include('amtrak.urls')),
]
