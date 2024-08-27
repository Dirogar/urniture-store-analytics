from django.urls import path

from .views import (ShopProductListView, CommentList,
                    StoreProductCommentListView, AddCommentView,
                    change_comment_status, update_store_info)

app_name = 'reports'

urlpatterns = [
    path('', ShopProductListView.as_view(), name='auth'),
    path('products/', ShopProductListView.as_view(), name='products'),
    path('comments/', CommentList.as_view(), name='all_comments'),
    path(
        'comments/<int:store_id>/<str:product_article>/',
        StoreProductCommentListView.as_view(),
        name='comments'
    ),
    path(
        'comments/<int:store_id>/<str:product_article>/add',
        AddCommentView.as_view(),
         name='add_comment'
    ),
    path(
        'api/change_comment_status/',
        change_comment_status,
        name='change_comment_status'
    ),
    path(
        'api/store_info/',
        update_store_info,
        name='update_store_info'
    ),
]
