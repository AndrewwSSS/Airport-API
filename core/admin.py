from django.contrib import admin

from core.models import Airplane
from core.models import AirplaneType
from core.models import Airport
from core.models import City
from core.models import Country
from core.models import Crew
from core.models import Flight
from core.models import Order
from core.models import Route
from core.models import Ticket
from user.models import User


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Crew)
admin.site.register(Order)
admin.site.register(Flight)
admin.site.register(Ticket)
