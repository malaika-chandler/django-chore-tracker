from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from chores_list import models, forms
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)


class ChoreListView(LoginRequiredMixin, ListView):
    model = models.Chore
    template_name = 'chores_list/chore_list.html'


class ChoreDetailView(LoginRequiredMixin, DetailView):
    model = models.Chore
    template_name = 'chores_list/chore_detail.html'


class ChoreCreateView(LoginRequiredMixin, CreateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = forms.ChoreIntervalForm()
        return context


class ChoreUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')


class ChoreDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Chore
    success_url = reverse_lazy("chores_list:chore_list")
