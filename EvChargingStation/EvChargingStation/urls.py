from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from EvCharging import views

urlpatterns = [
    # 1. Admin & Core Auth
    path('admin/', admin.site.urls), # Re-enabled!
    path('', views.log, name='login'),
    path('login_post', views.login_post),
    path('logout', views.logout),
    path('forgot_password', views.forgot_password),
    path('forgot_password_post', views.forgot_password_post),

    # 2. Admin Dashboard Views
    path('admin_index', views.admin_index),
    path('admin_analytics', views.analytics_dashboard),
    path('station_detail/<int:station_id>', views.station_detail),
    path('submit_rating/<int:station_id>', views.submit_rating),
    path('send_reply/<id>', views.send_reply),
    path('send_reply_post/<id>', views.send_reply_post),
    path('view_charging_station', views.view_charging_station),
    path('view_compalaint', views.view_complaint),
    path('view_rating_admin', views.view_rating_admin),
    path('view_rejected_charging_station', views.view_rejected_charging_station),
    path('view_user', views.view_user),
    path('view_verified_charging_station', views.view_verified_charging_station),
    path('approved_charging/<id>', views.approved_charging),
    path('rejected_charging/<id>', views.rejected_charging),

    path('add_charge', views.add_charge),
    path('add_charge_post', views.add_charge_post),
    path('add_charging_slot/<id>', views.add_charging_slot),
    path('add_charging_slot_post/<id>', views.add_charging_slot_post),
    path('add_time_slot', views.add_time_slot),
    path('add_time_slot_post', views.add_time_slot_post),
    path('edit_time_slot/<id>', views.edit_time_slot),
    path('edit_time_slot_post/<id>', views.edit_time_slot_post),
    path('remove_charge/<id>', views.remove_charge),
    path('remove_time_slot/<id>', views.remove_time_slot),
    path('edit_charge/<id>', views.edit_charge),
    path('edit_charge_post/<id>', views.edit_charge_post),
    path('edit_charging_slot/<id>', views.edit_charging_slot),
    path('edit_charging_slot_post/<id>', views.edit_charging_slot_post),
    path('delete_charging_slot/<id>', views.delete_charging_slot),
    
    # 4. User/Station Interface
    path('station_map', views.station_map),
    path('view_available_slot', views.view_available_slot),
    path('view_booking', views.view_booking),
    path('view_charge', views.view_charge),
    path('view_charging_slot/<id>', views.view_charging_slot),
    path('charging_station_view_payment', views.charging_station_view_payment),
    path('charging_station_view_payment_post', views.charging_station_view_payment_post),
    path('view_profile', views.view_profile),
    path('view_rating', views.view_rating),
    path('view_time_slot', views.view_time_slot),
    path('home_charging_station', views.home_charging_station),

    # 5. Android API Endpoints (Keep these for the "Mobile-Ready" pitch)
    path('and_login', views.and_login),
    path('and_reset_password', views.and_reset_password),
    path('and_user_register', views.and_user_register),
    path('and_send_complaint', views.and_send_complaint),
    path('and_send_rating', views.and_send_rating),
    path('and_view_available_slot', views.and_view_available_slot),
    path('and_view_charging_slot', views.and_view_charging_slot),
    path('and_view_reply', views.and_view_reply),
    path('and_view_nearby_charging_station', views.and_view_nearby_charging_station),
    path('and_view_previous_booking', views.and_view_previous_booking),
    path('and_view_profile', views.and_view_profile),
    path('and_view_available_timeslot', views.and_view_available_timeslot),
    path('and_offline_payment', views.and_offline_payment),
    path('android_online_payment', views.android_online_payment),
    path('and_view_slot_with_date', views.and_view_slot_with_date),
]

# CRITICAL: This serves images and CSS during the demo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)