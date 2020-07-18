from django.contrib import admin
from chores.models import Chore, ChoreInterval, ChoreInstance


class ChoreIntervalInline(admin.TabularInline):
    model = ChoreInterval


class ChoreInstanceInline(admin.TabularInline):
    model = ChoreInstance


# Register your models here.
admin.site.register(Chore)
admin.site.register(ChoreInterval)
admin.site.register(ChoreInstance)
