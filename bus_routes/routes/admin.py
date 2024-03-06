from django.contrib import admin
from .models import Bus, Stop, Route, Ticket, Company, Schedule, RouteStop
# Register your models here.


admin.site.register(Bus)
admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(Company)
admin.site.register(Schedule)
admin.site.register(RouteStop)
