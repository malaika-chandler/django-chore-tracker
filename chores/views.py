from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views import generic
from datetime import timedelta, datetime
import calendar
from chores import models, forms


# User = get_user_model()


class AllChoreListView(generic.ListView):
    model = models.Chore
    template_name = 'chores/chore_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'All Chores'
        context['empty_message'] = 'No chores to display!'
        return context

    def get_queryset(self):
        return models.Chore.objects.all().order_by('datetime')


class CompletedChoreListView(generic.ListView):
    model = models.Chore
    template_name = 'chores/chore_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Completed Chores'
        context['empty_message'] = 'No chores to display!'
        return context

    def get_queryset(self):
        return models.Chore.objects.filter(completed=True).order_by('datetime')


class ChoreListView(generic.ListView):
    model = models.Chore
    template_name = 'chores/chore_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Upcoming Chores"
        context['empty_message'] = 'No upcoming instances to display!'
        return context

    def get_queryset(self):
        now = timezone.now()
        week_later = now + timedelta(days=7)
        return models.Chore.objects.filter(
            instances__datetime__range=(now, week_later),
            instances__done=False
        ).order_by('instances__datetime')


class ChoreInstanceListView(generic.ListView):
    model = models.ChoreInstance
    template_name = 'chores/chore_instance_list.html'
    context_object_name = 'chore_instance_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Upcoming Chores"
        context['empty_message'] = 'No upcoming instances to display!'
        return context

    def get_queryset(self):
        now = timezone.now()
        week_later = now + timedelta(days=7)
        return models.ChoreInstance.objects.filter(
            datetime__range=(now, week_later),
            done=False
        ).order_by('datetime')


class CompletedChoreInstanceListView(generic.ListView):
    model = models.ChoreInstance
    template_name = 'chores/chore_instance_list.html'
    context_object_name = 'chore_instance_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Completed Occurrences"
        context['empty_message'] = "No completed occurrences to display"
        return context

    def get_queryset(self):
        return models.ChoreInstance.objects.filter(
            done=True
        ).order_by('datetime')


class ChoreDetailView(generic.DetailView):
    model = models.Chore
    template_name = 'chores/chore_detail.html'


class ChoreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Chore
    success_url = reverse_lazy("chores:total_chore_list")


def mark_chore_complete(request, pk):
    if request.method == 'POST':
        chore = get_object_or_404(models.Chore, pk=pk)

        # Remove any unfinished instances
        models.ChoreInstance.objects.filter(chore=chore.pk).delete()

        chore.completed = True
        chore.last_completed_by = request.user
        chore.last_completed_on = timezone.now()

        chore.save()

        data = {
            'success': True
        }
        return JsonResponse(data)

    elif request.method == 'GET':
        chore = get_object_or_404(models.Chore, pk=pk)

        # Remove any unfinished instances
        models.ChoreInstance.objects.filter(chore=chore.pk, done=False).delete()

        chore.completed = True
        chore.last_completed_by = request.user
        chore.last_completed_on = timezone.now()

        chore.save()

        return redirect(request.META['HTTP_REFERER'] or 'chores:chore_detail', pk=chore.pk)

    raise Http404("")


def mark_chore_instance_complete(request, pk):
    if request.method == 'POST':
        chore_instance = get_object_or_404(models.ChoreInstance, pk=pk)
        chore_instance.done = True
        chore_instance.save()

        chore = models.Chore.objects.get(pk=chore_instance.chore.pk)
        chore.last_completed_by = request.user
        chore.last_completed_on = timezone.now()
        chore.count_repetitions += 1
        chore.save()

        data = {
            'success': True
        }
        return JsonResponse(data)

    raise Http404("")


def delete_chore_instance(request, pk):
    if request.method == 'POST':
        chore_instance = get_object_or_404(models.ChoreInstance, pk=pk)
        num_deleted, _ = chore_instance.delete()

        data = {
            'success': num_deleted > 0
        }
        return JsonResponse(data)

    return Http404()


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
                models.ChoreInstance(
                    chore=chore,
                    interval=chore_interval,
                    datetime=(chore.datetime + (delta * dt))
                )
                for dt in range(count)
            ]

        elif chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.YEARLY:
            instances = []
            new_date = datetime.fromtimestamp(chore.datetime.timestamp(), tz=timezone.get_default_timezone())
            for i in range(count):
                new_year = new_date.year + i
                # Just in case a month doesn't contain enough days, get the max for that month instead
                # Mainly just for events starting Feb 29 and recurring every year
                new_day = min(new_date.day, calendar.monthrange(new_year, new_date.month)[1])

                instances.append(
                    models.ChoreInstance(
                        chore=chore,
                        interval=chore_interval,
                        datetime=(new_date.replace(year=new_year, day=new_day))
                    )
                )

        elif chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.MONTHLY:
            instances = []
            new_date = datetime.fromtimestamp(chore.datetime.timestamp(), tz=timezone.get_default_timezone())
            for i in range(count):
                new_month = new_date.month + i
                new_year = new_date.year
                if new_month > 12:
                    new_year += int(new_month / 12)  # integer division to get proper year increment
                    # python months go from 1..12, not 0..11
                    new_month = new_month % 12 if new_month % 12 != 0 else 12

                # Just in case a month doesn't contain enough days, get the max for that month instead
                new_day = min(new_date.day, calendar.monthrange(new_year, new_month)[1])

                instances.append(
                    models.ChoreInstance(
                        chore=chore,
                        interval=chore_interval,
                        datetime=(new_date.replace(year=new_year, month=new_month, day=new_day))
                    )
                )

        elif chore_interval.repeat_interval == models.ChoreInterval.IntervalChoice.WEEK_DAILY:
            instances = []
            new_date = datetime.fromtimestamp(chore.datetime.timestamp(), tz=timezone.get_default_timezone())
            day_count = 0
            while len(instances) < count:
                next_day = new_date + timedelta(days=day_count)
                if next_day.weekday() in range(5):  # 0 is Monday and 4 is Friday
                    instances.append(
                        models.ChoreInstance(
                            chore=chore,
                            interval=chore_interval,
                            datetime=next_day
                        )
                    )
                day_count += 1

        else:
            print("Something has gone wrong with instances")

    else:
        instances.append(models.ChoreInstance(chore=chore, interval=None, datetime=chore.datetime))

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

    return render(request, 'chores/chore_form.html', {
        'chore_form': chore_form,
        'interval_form': interval_form,
        'page_title': "Create A New Chore",
    })


def edit_chore(request, pk):
    chore = get_object_or_404(models.Chore, pk=pk)
    interval = models.ChoreInterval.objects.filter(chore=chore.pk)
    if request.method == 'POST':
        chore_form = forms.ChoreForm(request.POST, instance=chore)
        if interval:
            interval_form = forms.ChoreIntervalForm(request.POST, instance=interval[0])
        else:
            interval_form = forms.ChoreIntervalForm(request.POST)

        if chore_form.is_valid():
            # Chore had intervals but now no longer repeats
            if not chore_form.cleaned_data['repeats'] and chore.chore_intervals.count() > 0:
                chore = chore_form.save()
                models.ChoreInterval.objects.filter(chore=chore.pk).delete()
                # delete occurrences from old interval that weren't marked complete
                models.ChoreInstance.objects.filter(chore=chore.pk, interval=None, done=False).delete()
                return redirect('chores:chore_detail', pk=chore.pk)

            elif not chore_form.cleaned_data['repeats']:
                chore = chore_form.save()
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
                chore = chore_form.save()
                return redirect('chores:chore_detail', pk=chore.pk)

    else:
        chore_form = forms.ChoreForm(instance=chore)
        if interval:
            interval = interval[0]
            interval_form = forms.ChoreIntervalForm(instance=interval)
        else:
            interval_form = forms.ChoreIntervalForm()

    return render(request, 'chores/chore_form.html', {
        'chore_form': chore_form,
        'interval_form': interval_form,
        'page_title': "Update Chore",
    })
