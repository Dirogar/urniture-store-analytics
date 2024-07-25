import json

from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from http import HTTPStatus
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic.detail import SingleObjectMixin
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import Store, Comment, User, Product, Warehouse, StoreProduct
from .forms import CommentForm


class ShopProductListView(LoginRequiredMixin, ListView):
    """Отображает таблицу с данными"""
    template_name = 'reports/product_list2.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 10


    def get_queryset(self):
        """Возвращает связанные данные"""
        user = self.request.user
        stores = user.stores.all()
        queryset = Product.objects.prefetch_related(
            'warehouse_products', 'store_products'
        ).filter(
            Q(store_products__store__users=user)
        ).distinct()
        sort_by = self.request.GET.get('sort', 'article')
        order = self.request.GET.get('order', 'asc')

        if order == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает связанные данные магазинов-продукутов, складов-продуктов
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['stores'] = user.stores.all()
        context['warehouses'] = Warehouse.objects.all()
        context['current_sort'] = self.request.GET.get('sort', 'default')
        context['current_order'] = self.request.GET.get('order', 'asc')

        warehouse_data = {}
        store_data = {}
        comments_data = {}

        for product in context['products']:
            warehouse_data[product.article] = {
                wp.warehouse_id: wp.stock for wp
                in product.warehouse_products.all()
            }
            store_data[product.article] = {sp.store_id: sp for sp in
                                           product.store_products.all()}
            for store in context['stores']:
                comments = Comment.objects.filter(store=store, product=product).order_by('-created_at')
                if comments.exists():
                    if product.article not in comments_data:
                        comments_data[product.article] = {}
                    comments_data[product.article][store.id] = comments.count()

        context['warehouse_data'] = warehouse_data
        context['store_data'] = store_data
        context['comments_data'] = comments_data

        return context


class StoreProductCommentListView(LoginRequiredMixin, ListView):
    template_name = 'reports/store_product_comments.html'
    context_object_name = 'comments'


    def get_queryset(self):
        """Возвращает страницу с комментарием товара"""
        store_id = self.kwargs['store_id']
        product_article = self.kwargs['product_article']
        return Comment.objects.filter(
            store_id=store_id, product__article=product_article
        ).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        store_id = self.kwargs['store_id']
        product_article = self.kwargs['product_article']


        store = Store.objects.get(id=store_id)
        product = Product.objects.get(article=product_article)

        context['store'] = store
        context['product'] = product
        context['form'] = CommentForm()
        return context


class AddCommentView(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'includes/comment_form.html'

    def form_valid(self, form):
        """Добавляет в поля формы автора, товар и магазин"""
        form.instance.author = self.request.user
        store_id = self.kwargs.get('store_id')
        product_article = self.kwargs.get('product_article')
        product = get_object_or_404(Product, article=product_article)
        form.instance.product = product
        form.instance.store_id = store_id
        self.object = form.save()

        data = {
            'author': {'id': self.object.author.id,
                       'username': self.object.author.username},
            'text': self.object.text,
            'created_at': self.object.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'finish_planned_date': self.object.finish_planned_date
        }
        return JsonResponse(data)


    def get_success_url(self):
        return self.request.path


class CommentList(LoginRequiredMixin, ListView):
    """Возвращает список всех комментариев"""
    model = Comment
    template_name = 'reports/comments_list.html'
    context_object_name = 'all_comments'


    def get_queryset(self):
        queryset = Comment.objects.select_related(
            'product', 'store'
        )
        return queryset




@csrf_exempt
def update_store_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_article = data.get('product')
        store_id = data.get('store')
        value = data.get('value')
        field = data.get('field')
        try:
            if field == 'room_class':
                product = Product.objects.get(article=product_article)
                setattr(product, field, value)
                product.save()
            else:
                store_product = StoreProduct.objects.get(product__article=product_article, store_id=store_id)
                setattr(store_product, field, value)
                store_product.save()
            return JsonResponse({'success': True})
        except Exception as e:
            raise e





