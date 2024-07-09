from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from http import HTTPStatus
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic.detail import SingleObjectMixin

from .models import Shops, Comment, User
from .forms import CommentForm


class MainPage(LoginRequiredMixin, ListView):
    model = Shops
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
        return Shops.objects.filter(members=self.request.user)


class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = CommentForm
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'comment_text': self.object.text})

    def form_invalid(self, form):
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
