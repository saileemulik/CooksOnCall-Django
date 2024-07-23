from django.contrib import admin
from .models import Contact,Single,TeamCook,Booking,Payment
# Register your models here.
admin.site.register(Contact)
admin.site.register(Single)
admin.site.register(TeamCook)
admin.site.register(Booking)
admin.site.register(Payment)
# admin.site.register(CustomUser)