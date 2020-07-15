from django.shortcuts import render
from django.urls import reverse_lazy
from chores_list import models
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)


class ChoreListView(ListView):
    model = models.Chore
    template_name = 'chores_list/chore_list.html'


class ChoreDetailView(DetailView):
    model = models.Chore
    template_name = 'chores_list/school_detail.html'


class ChoreCreateView(CreateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')


class ChoreUpdateView(UpdateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')


class ChoreDeleteView(DeleteView):
    model = models.Chore
    success_url = reverse_lazy("chore_list:list")

