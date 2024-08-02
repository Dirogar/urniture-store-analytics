"""
Основные представления приложения reports.

Приложение отображает сводную таблицу с ограничением доступа, а так же
возможность комментировать данные в пересечениях.
Где строки - это товар (таблица Product)
Столбцы - это Склады, Магазины (таблицы Warehouse, Store)
"""
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
    paginate_by = 20


    def get_queryset(self):
        """Возвращает связанные данные"""
        user = self.request.user
        stores = user.store.all()
        queryset = Product.objects.prefetch_related(
            'warehouse_products', 'store_products'
        ).filter()
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
        context['stores'] = user.store.all().order_by('name')
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
                comments = Comment.objects.filter(
                    store=store,
                    product=product
                ).order_by('-created_at')
                if comments.exists():
                    if product.article not in comments_data:
                        comments_data[product.article] = {}
                    comments_data[product.article][store.id] = comments.count()

        context['warehouse_data'] = warehouse_data
        context['store_data'] = store_data
        context['comments_data'] = comments_data

        return context


class StoreProductCommentListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения комментариев к товару в конкретном магазине.

    Это представление требует, чтобы пользователь был аутентифицирован.
    Оно использует шаблон 'reports/store_product_comments.html' и передает в контекст
    переменную 'comments', содержащую комментарии.
    """

    template_name = 'reports/store_product_comments.html'
    context_object_name = 'comments'


    def get_queryset(self):
        """
        Возвращает QuerySet с комментариями к указанному товару
         в указанном магазине.

        Этот метод фильтрует комментарии по идентификатору магазина и
        артикулу товара,
        сортируя их по дате создания в порядке убывания.

        :return: QuerySet с комментариями к товару в магазине.
        """
        store_id = self.kwargs['store_id']
        product_article = self.kwargs['product_article']
        return Comment.objects.filter(
            store_id=store_id, product__article=product_article
        ).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Добавляет дополнительные данные в контекст шаблона.

        Этот метод добавляет в контекст данные о магазине, товаре и форму для
         добавления комментария.

        :param object_list: Список объектов (необязательно).
        :param kwargs: Дополнительные аргументы контекста.
        :return: Обновленный контекст шаблона.
        """
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
    """
    Представление для добавления нового комментария.

    Это представление использует форму `CommentForm` и шаблон
    'includes/comment_form.html'.
    """
    form_class = CommentForm
    model = Comment
    template_name = 'includes/comment_form.html'

    def form_valid(self, form):
        """
        Обрабатывает валидную форму, добавляя автора, товар и магазин к
        комментарию.

        Этот метод добавляет текущего пользователя как автора комментария,
        а также связывает комментарий с товаром и магазином, основываясь на
        параметрах URL. После сохранения комментария, возвращает JSON-ответ
        с данными комментария.

        :param form: Валидная форма комментария.
        :return: JsonResponse с данными сохраненного комментария.
        """
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
        """
        Возвращает URL для перенаправления после успешного сохранения формы.

        Этот метод возвращает текущий URL, что позволяет оставаться на той же
        странице после выполнения всех условий.

        :return: Текущий URL запроса.
        """
        return self.request.path


class CommentList(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка всех комментариев.

    Это представление требует, чтобы пользователь был аутентифицирован.
    Оно использует шаблон 'reports/comments_list.html' и передает в контекст
    переменную 'all_comments', содержащую все комментарии.
    """

    model = Comment
    template_name = 'reports/comments_list.html'
    context_object_name = 'all_comments'

    def get_queryset(self):
        """
        Возвращает QuerySet с комментариями, включающими связанные данные.

        Этот метод возвращает QuerySet, который включает связанные объекты
        'product' и 'store' для каждого комментария, отсортированные по
        дате создания в порядке убывания.

        :return: QuerySet с комментариями и связанными объектами 'product' и
        'store'.
        """
        queryset = Comment.objects.select_related(
            'product', 'store'
        ).order_by('-created_at')
        return queryset


@csrf_exempt
def update_store_product(request) -> JsonResponse:
    """
    Добавляет значения в таблицу Store и Product.

    :param request: Запрос на добавление/изменение данных
    :return: Json с результатом выполнения запроса
    """
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
                store_product = StoreProduct.objects.get(
                    product__article=product_article, store_id=store_id
                )
                setattr(store_product, field, value)
                store_product.save()
            return JsonResponse({'success': True})
        except Exception as e:
            raise e


@csrf_exempt
def change_comment_status(request) -> JsonResponse:
    """
    Возвращает новый статус комментария.

    :param request: Запрос на изменение статуса при нажатии на кнопку
    "статус" у комментария
    :return: Json с результатом выполнения запроса
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        comment_id = data.get('comment_id')

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse(
                {'success': False, 'error': 'Comment not found'},
                status=HTTPStatus.NOT_FOUND
            )

        current_status = comment.status
        if current_status == 'Выполнено':
            current_status = 'Не выполнено'
        elif current_status == 'В работе':
            current_status = 'Выполнено'
        else:
            current_status = 'В работе'
        comment.status = current_status
        comment.save()
        return JsonResponse(
            {'success': True, 'comment_id': comment.id,
             'new_status': comment.status}
        )
    return JsonResponse(
        {'success': False, 'error': 'Invalid request'},
        status=HTTPStatus.NOT_FOUND
    )
