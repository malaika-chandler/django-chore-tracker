from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from chores import models, forms
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)


class ChoreListView(ListView):
    model = models.Chore
    template_name = 'chores/chore_list.html'


class ChoreDetailView(DetailView):
    model = models.Chore
    template_name = 'chores/chore_detail.html'


class ChoreCreateView(LoginRequiredMixin, CreateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')
    redirect_field_name = 'chores/chore_detail.html'
    template_name = 'chores/create_chore_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = forms.ChoreIntervalForm()
        return context


class ChoreUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')
    redirect_field_name = 'chores/chore_detail.html'
    template_name = 'chores/update_chore_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interval = models.ChoreInterval.objects.filter(chore=context['object'].pk).first()
        print('TEST', forms.ChoreIntervalForm(interval))
        context['form2'] = forms.ChoreIntervalForm(interval)
        return context


class ChoreDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Chore
    success_url = reverse_lazy("chores:chore_list")
