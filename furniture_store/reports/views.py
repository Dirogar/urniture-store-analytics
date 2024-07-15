from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from http import HTTPStatus
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic.detail import SingleObjectMixin

from .models import Store, Comment, User, Product, Warehouse
from .forms import CommentForm



class ShopProductListView(LoginRequiredMixin, ListView):
    """Отображает таблицу с данными"""
    template_name = 'reports/product_list2.html'
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        """Возвращает связанные данные"""
        return Product.objects.prefetch_related(
            'warehouseproduct_set', 'storeproduct_set'
        ).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stores'] = Store.objects.all()
        context['warehouses'] = Warehouse.objects.all()

        warehouse_data = {}
        store_data = {}

        for product in context['products']:
            warehouse_data[product.article] = {wp.warehouse_id: wp.stock for wp in product.warehouseproduct_set.all()}
            store_data[product.article] = {sp.store_id: sp for sp in product.storeproduct_set.all()}

        context['warehouse_data'] = warehouse_data
        context['store_data'] = store_data

        return context


class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновляет комментарий"""
    form_class = CommentForm
    model = Comment

    def test_func(self):
        """Проверяет что пользователь автор коммента"""
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        """Валидирует форму и сохраняет значение"""
        self.object = form.save()
        return JsonResponse({'comment_text': self.object.text})

    def form_invalid(self, form):
        """Возвращает ошибку при невалидности"""
        return JsonResponse({'error': form.errors},
                            status=HTTPStatus.BAD_REQUEST)


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('reports:index')
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
