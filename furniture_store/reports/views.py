from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Shops


class MainPage(LoginRequiredMixin, ListView):
    model = Shops
    template_name = 'reports/shop_list.html'
    redirect_field_name = 'redirect_to'
