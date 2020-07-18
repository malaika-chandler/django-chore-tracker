from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import generic
from datetime import timedelta, datetime
import calendar
from chores import models, forms


class ChoreListView(generic.ListView):
    model = models.Chore
    template_name = 'chores/chore_list.html'

    def get_queryset(self):
        # if self.kwargs['']:
        now = timezone.now()
        week_later = now + timedelta(days=7)
        return models.Chore.objects.filter(
            instances__datetime__range=(now, week_later), instances__done=False).order_by('instances__datetime')

        # return models.Chore.objects.all()


class ChoreDetailView(generic.DetailView):
    model = models.Chore
    template_name = 'chores/chore_detail.html'


class ChoreCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')
    redirect_field_name = 'chores/chore_detail.html'
    template_name = 'chores/create_chore_form.html'


class ChoreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Chore
    fields = ('name', 'description', 'repeats')
    redirect_field_name = 'chores/chore_detail.html'
    template_name = 'chores/update_chore_form.html'


class ChoreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Chore
    success_url = reverse_lazy("chores:chore_list")


def generate_instances(chore, chore_interval, count=20):
    instances = []
    if chore_interval is not None:
        if (chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.DAILY
                or chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.WEEKLY
                or chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.CUSTOM):
            if chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.DAILY:
                delta = timedelta(days=1)
            elif chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.WEEKLY:
                delta = timedelta(days=7)
            else:
                delta = timedelta(days=chore_interval.repeat_custom_interval)

            instances = [
                models.ChoreInstance(chore=chore, interval=chore_interval, datetime=(chore.datetime + (delta * dt)))
                for dt in range(count + 1)
            ]

        elif chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.YEARLY:
            instances = []
            new_date = datetime.fromtimestamp(chore.datetime)
            for i in range(count + 1):
                instances.append(new_date.replace(year=new_date.year + i))

        elif chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.MONTHLY:
            instances = []
            new_date = datetime.fromtimestamp(chore.datetime)
            for i in range(count + 1):
                instances.append(new_date.replace(month=new_date.month + i))

        elif chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.WEEK_DAILY:
            instances = []
            new_date = datetime.fromtimestamp(chore.datetime)
            day_count = 0
            while len(instances) < count:
                next_day = new_date.replace(day=new_date.day + day_count)
                if next_day.weekday() in range(5):  # 0 is Monday and 4 is Friday
                    instances.append(next_day)
                day_count += 1

        else:
            print("Something has gone wrong with instances")

        return instances


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

                chore_instances = generate_instances(chore, chore_interval)
                models.ChoreInstance.objects.bulk_create(chore_instances)
                return redirect('chores:chore_detail', pk=chore.pk)
            elif not chore_form.cleaned_data['repeats']:
                chore = chore_form.save()
                chore_instance = models.ChoreInstance(chore=chore, interval=None, datetime=chore.datetime)
                chore_instance.save()
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
            # Chore had intervals but now no longer repeats
            if not chore_form.cleaned_data['repeats'] and chore.chore_intervals.count() > 0:
                chore = chore_form.save()
                models.ChoreInterval.objects.filter(chore=chore.pk).delete()
                # delete occurrences from old interval that weren't marked complete
                models.ChoreInstance.objects.filter(chore=chore.pk, interval=None, done=False).delete()
                return redirect('chores:chore_detail', pk=chore.pk)

            # Chore repeats, but the interval has changed
            elif chore_form.cleaned_data['repeats'] and interval_form.has_changed() and interval_form.is_valid():
                chore = chore_form.save()
                chore_interval = interval_form.save(commit=False)
                chore_interval.chore = chore
                chore_interval.save()

                # handle any existing instances and create more
                models.ChoreInstance.objects.filter(chore=chore.pk, done=False).delete()
                chore_instances = generate_instances(chore, chore_interval)
                models.ChoreInstance.objects.bulk_create(chore_instances)

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
