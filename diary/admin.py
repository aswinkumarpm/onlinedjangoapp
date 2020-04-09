from django.contrib import admin

# Register your models here.
from diary.models import Registration, Diary, Contact

admin.site.register(Registration)
admin.site.register(Diary)
admin.site.register(Contact)
