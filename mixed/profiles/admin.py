from django.contrib import admin
from django.contrib import admin
from .models import Profile, PartnerProfile

# Register your models here.

class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'partner')
    list_display_links = ('id', 'company_name', 'partner')


admin.site.register(Profile)
admin.site.register(PartnerProfile, PartnerProfileAdmin)
