from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from .models import Shops


class MainPage(ListView):
    model = Shops
    template_name = 'reports/shop_list.html'

