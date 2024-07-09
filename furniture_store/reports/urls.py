from django.urls import path

from .views import MainPage, EditCommentView, DeleteCommentView

app_name = 'reports'

urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('comment/<int:pk>/edit/', EditCommentView.as_view(),
         name='comment_edit'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(),
         name='comment_delete'),
]
