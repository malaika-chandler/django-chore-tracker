from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
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


class ChoreUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')
    redirect_field_name = 'chores/chore_detail.html'
    template_name = 'chores/update_chore_form.html'


class ChoreDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Chore
    success_url = reverse_lazy("chores:chore_list")


def submit_new_chore(request):
    if request.method == 'POST':
        chore_form = forms.ChoreForm(request.POST)
        interval_form = forms.ChoreIntervalForm(request.POST)
        if chore_form.is_valid():
            if chore_form.cleaned_data['repeats'] and interval_form.is_valid():
                chore = chore_form.save()
                chore_interval = interval_form.save(commit=False)
                chore_interval.chore = chore
                chore_interval.save()
                return redirect('chores:chore_detail', pk=chore.pk)
            elif not chore_form.cleaned_data['repeats']:
                chore = chore_form.save()
                return redirect('chores:chore_detail', pk=chore.pk)
    else:
        chore_form = forms.ChoreForm()
        interval_form = forms.ChoreIntervalForm()

    return render(request, 'chores/create_chore_form.html', {
        'chore_form': chore_form,
        'interval_form': interval_form
    })


def edit_chore(request, pk):
    chore = get_object_or_404(models.Chore, pk=pk)
    interval = models.ChoreInterval.objects.filter(chore=chore.pk)
    if request.method == 'POST':
        chore_form = forms.ChoreForm(request.POST)
        interval_form = forms.ChoreIntervalForm(request.POST)
        if chore_form.is_valid():
            if not chore_form.cleaned_data['repeats'] and chore.chore_intervals.count() > 0:
                print("Has intervals but no longer repeats")
                chore = chore_form.save()
                models.ChoreInterval.objects.filter(chore=chore.pk).delete()
                return redirect('chores:chore_detail', pk=chore.pk)
            elif chore_form.cleaned_data['repeats'] and interval_form.is_valid():
                chore = chore_form.save()
                chore_interval = interval_form.save(commit=False)
                chore_interval.chore = chore
                chore_interval.save()
                return redirect('chores:chore_detail', pk=chore.pk)
    else:
        chore_form = forms.ChoreForm(instance=chore)
        if interval:
            interval = interval[0]
            interval_form = forms.ChoreIntervalForm(instance=interval)
        else:
            interval_form = forms.ChoreIntervalForm()

    return render(request, 'chores/update_chore_form.html', {
        'chore_form': chore_form,
        'interval_form': interval_form
    })
