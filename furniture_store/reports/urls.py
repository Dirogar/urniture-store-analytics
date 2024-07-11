from django.urls import path

from .views import MainPage, EditCommentView, DeleteCommentView, ShopProductListView

app_name = 'reports'

urlpatterns = [
    path('', ShopProductListView.as_view(), name='products'),
    path('products/', ShopProductListView.as_view(), name='products'),
    path('comment/<int:pk>/edit/', EditCommentView.as_view(),
         name='comment_edit'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(),
         name='comment_delete'),

]
