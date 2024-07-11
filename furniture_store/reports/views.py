from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from http import HTTPStatus
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic.detail import SingleObjectMixin

from .models import Shop, Comment, User, Product
from .forms import CommentForm


class MainPage(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'reports/shop_list.html'
    redirect_field_name = 'redirect_to'
    context_object_name = 'shops'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.shop_id = request.POST.get('shop_id')
            comment.save()
            return redirect(reverse('reports:index'))
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        return Shop.objects.filter(members=self.request.user)


class ShopProductListView(LoginRequiredMixin, ListView):
    """Отображает таблицу с данными"""
    template_name = 'reports/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Добавляет к товарам связанные таблицы"""
        shops = Product.objects.prefetch_related('shops').all()
        return shops


class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Позволяет обновлять комментарии"""
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
