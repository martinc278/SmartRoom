from django.contrib import admin

from .models import Chair, Measure

# Register your models here.
class ChairAdmin(admin.ModelAdmin):
    fields = ['idc', 'ip']
    list_display = ('idc', 'ip')
    list_filter = ['ip']
    search_fields = ['idc', 'ip']

class MeasureAdmin(admin.ModelAdmin):
    fields = ['idc', 'date', 'sensor_distance', 'sensor_temperature']
    list_display = ('idc', 'date', 'was_measured_recently')
    list_filter = ['date']


admin.site.register(Chair, ChairAdmin)
admin.site.register(Measure, MeasureAdmin)
