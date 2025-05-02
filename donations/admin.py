# donations/admin.py
from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'amount', 'donation_date', 'is_verified')
    list_filter = ('is_verified', 'donation_date')
    search_fields = ('donor__email', 'transaction_id')
    readonly_fields = ('transaction_id', 'donation_date')