from django.contrib import admin
from .models import Race, Runner, Result


class RaceAdmin(admin.ModelAdmin):
    pass


class RunnerAdmin(admin.ModelAdmin):
    pass


class ResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(Race, RaceAdmin)
admin.site.register(Runner, RunnerAdmin)
admin.site.register(Result, ResultAdmin)
