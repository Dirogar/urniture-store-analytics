from django.urls import path

from .views import (ShopProductListView, CommentList,
                    StoreProductCommentListView, AddCommentView,
                    update_store_product)

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
        'update_store_product/',
        update_store_product,
        name='update_store_product'
    ),
]
