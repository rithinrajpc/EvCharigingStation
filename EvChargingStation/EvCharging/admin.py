from django.contrib import admin
from .models import (
    Login,
    ChargingStation,
    TimeSlot,
    Charge,
    ChargingSlot,
    User,
    Rating,
    Complaint,
    Booking,
    Payment,
)


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'usertype')
    search_fields = ('username', 'usertype')


@admin.register(ChargingStation)
class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'contact', 'place', 'login')
    search_fields = ('name', 'email', 'place')


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'start_time', 'end_time', 'total_slot', 'charging_station')


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'fare', 'charging_station')


@admin.register(ChargingSlot)
class ChargingSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot_no', 'status', 'time_slot')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'contact', 'place', 'login')
    search_fields = ('name', 'email')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'rate', 'date', 'charging_station', 'user')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'complaint', 'reply', 'complaint_date', 'reply_date', 'user')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'user', 'charging_slot')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'date', 'type')
