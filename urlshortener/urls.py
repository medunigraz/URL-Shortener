from django.urls import path

from . import views
app_name="urlshortener"
urlpatterns = [
    path('', views.table_view, name='tableView'),
    path('detail/<str:id>/', views.detail_view, name='detailView'),
    path('detail/', views.detail_view, name='detailView'),
    path('redirect/<str:srcUrl>/', views.redirect_view, name='redirectView'),
    path('delete/', views.delete_view, name='deleteView'),
]