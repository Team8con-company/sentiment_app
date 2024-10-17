from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_results, name='search_results'),
    path('generate-wordcloud/', views.generate_wordcloud_api, name='generate_wordcloud_api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
