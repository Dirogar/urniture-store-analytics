from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from http import HTTPStatus
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse

from .models import Shops, Comment
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


class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if comment.author != request.user:
            return JsonResponse({'error': 'Permission denied'},
                                status=HTTPStatus.FORBIDDEN)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'Comment updated',
                                 'comment_text': comment.text})
        return JsonResponse({'error': 'Form is invalid'},
                            status=HTTPStatus.BAD_REQUEST)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
