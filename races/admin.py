from django.contrib import admin
from .models import Race, Runner, Result, Season, Classification, ClassificationResult, RecalculatedResult


class SeasonAdmin(admin.ModelAdmin):
    pass


class RaceAdmin(admin.ModelAdmin):
    pass


class RunnerAdmin(admin.ModelAdmin):
    pass


class ResultAdmin(admin.ModelAdmin):
    pass


class ClassificationAdmin(admin.ModelAdmin):
    pass


class ClassificationResultAdmin(admin.ModelAdmin):
    pass


class RecalculatedResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(Season, SeasonAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Runner, RunnerAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(ClassificationResult, ClassificationResultAdmin)
admin.site.register(RecalculatedResult, RecalculatedResultAdmin)
