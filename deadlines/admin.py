from django.contrib import admin

from .models import Bill


class BillAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'cost', 'expiry_date', 'payed', 'payed_date', 
	)
	list_filter = ('expiry_date', 'payed', 'payed_date')
	fieldsets = (
		('Dati bolletta', {
            'fields': (('title', 'cost', 'expiry_date'), ('payed', 'payed_date', 'payed_image'),)
        }),
    )

admin.site.register(Bill, BillAdmin)
