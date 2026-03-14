def analytics_dashboard(request):
    usage_labels = [s.name for s in ChargingStation.objects.all()]
    usage_data = [Booking.objects.filter(charging_slot__time_slot__charging_station=s).count() for s in ChargingStation.objects.all()]
    revenue_labels = usage_labels
    revenue_data = [Charge.objects.filter(charging_station=s).aggregate(models.Sum('fare'))['fare__sum'] or 0 for s in ChargingStation.objects.all()]
    activity_labels = ['Active', 'Inactive', 'New']
    activity_data = [User.objects.count(), ChargingStation.objects.count(), Login.objects.count()]
    return render(request, 'admin/analytics_dashboard.html', {
        'usage_labels': usage_labels,
        'usage_data': usage_data,
        'revenue_labels': revenue_labels,
        'revenue_data': revenue_data,
        'activity_labels': activity_labels,
        'activity_data': activity_data
    })
# -----------------------------
# STATION DETAIL & RATING
# -----------------------------
from django.views.decorators.csrf import csrf_protect

def station_detail(request, station_id):
    station = ChargingStation.objects.get(id=station_id)
    reviews = Rating.objects.filter(charging_station=station).select_related('user')
    avg_rating = reviews.aggregate(models.Avg('rate'))['rate__avg'] or 0
    return render(request, 'Charging Station/station_detail.html', {
        'station': station,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 2)
    })

@csrf_protect
def submit_rating(request, station_id):
    if request.method == 'POST':
        station = ChargingStation.objects.get(id=station_id)
        user = User.objects.get(login_id=request.session.get('lid'))
        rate = request.POST.get('rate')
        review = request.POST.get('review')
        Rating.objects.create(rate=rate, date=datetime.date.today(), charging_station=station, user=user, review=review)
        return redirect(f'/station_detail/{station_id}')
    return redirect(f'/station_detail/{station_id}')
# -----------------------------
# STATION MAP VIEW
# -----------------------------
def station_map(request):
    stations = ChargingStation.objects.filter(status='verified')
    return render(request, 'Charging Station/station_map.html', {'stations': stations})
import datetime
import smtplib
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import *


# -----------------------------
# AUTHENTICATION
# -----------------------------

def log(request):
    return render(request, "login index.html")


@csrf_exempt
def login_post(request):
    if request.method == "POST":
        # Template uses "textfield" / "textfield2" for username/password
        u = (request.POST.get('username') or request.POST.get('textfield') or "").strip()
        p = (request.POST.get('password') or request.POST.get('textfield2') or "").strip()

        # DEBUG: log what we received (visible in terminal output)
        print(f"[login_post] received username={u!r} password={p!r}")

        user_obj = Login.objects.filter(username=u, password=p).first()

        # If not found, allow login via charging station email or name (common UX expectation)
        if not user_obj:
            cs = ChargingStation.objects.filter(email=u).select_related('login').first()
            if cs and cs.login.password == p:
                user_obj = cs.login

        if not user_obj:
            cs = ChargingStation.objects.filter(name__iexact=u).select_related('login').first()
            if cs and cs.login.password == p:
                user_obj = cs.login

        if user_obj:
            request.session['lid'] = user_obj.id

            if user_obj.usertype == "admin":
                return redirect('/admin_index')

            elif user_obj.usertype == "chargingstation":
                return redirect('/home_charging_station')

        print(f"[login_post] invalid login for {u!r}")
        return HttpResponse("<script>alert('Invalid Login');window.location='/'</script>")

    return redirect('/')


def logout(request):
    request.session.flush()
    return HttpResponse("<script>alert('Logged out');window.location='/'</script>")


def forgot_password(request):
    return render(request, "Forgot Password.html")


@csrf_exempt
def forgot_password_post(request):
    Email = request.POST.get('textfield')
    data = Login.objects.filter(username=Email)

    if data.exists():

        pwd = data[0].password

        try:
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login("evcharginggstationn@gmail.com", "swvm ongk bwgk zlhp")

            msg = MIMEMultipart()
            msg['From'] = "evcharginggstationn@gmail.com"
            msg['To'] = Email
            msg['Subject'] = "Ev Charging Password"

            body = "Your password is : " + str(pwd)
            msg.attach(MIMEText(body, 'plain'))

            s.send_message(msg)
            s.quit()

            return HttpResponse("<script>alert('Password sent');window.location='/'</script>")

        except:
            return HttpResponse("<script>alert('Email error');window.location='/'</script>")

    return HttpResponse("<script>alert('User not found');window.location='/'</script>")


# -----------------------------
# ADMIN PANEL
# -----------------------------

def admin_index(request):
    return render(request, "admin/admin index.html")


def view_user(request):
    data = User.objects.all()
    return render(request, "admin/view user.html", {"data": data})


def view_complaint(request):
    data = Complaint.objects.all()
    return render(request, "admin/view complaint.html", {"data": data})


def send_reply(request, id):
    return render(request, "admin/send reply.html", {"id": id})


@csrf_exempt
def send_reply_post(request, id):
    reply = request.POST.get('textarea')
    date = datetime.datetime.now()

    Complaint.objects.filter(id=id).update(reply=reply, reply_date=date)

    return HttpResponse("<script>alert('Reply sent');window.location='/view_complaint'</script>")


def view_charging_station(request):
    data = ChargingStation.objects.all()
    return render(request, "admin/view charging station.html", {"data": data})


def view_rating_admin(request):
    data = Rating.objects.all()
    return render(request, "admin/view_rating_admin.html", {"data": data})


def view_verified_charging_station(request):
    data = ChargingStation.objects.filter(status="approved")
    return render(request, "admin/view verified charging station.html", {"data": data})


def view_rejected_charging_station(request):
    data = ChargingStation.objects.filter(status="rejected")
    return render(request, "admin/view rejected charging station.html", {"data": data})


def approved_charging(request, id):
    ChargingStation.objects.filter(id=id).update(status="approved")
    messages.success(request, "Charging station approved")
    return redirect('/view_charging_station')


def rejected_charging(request, id):
    ChargingStation.objects.filter(id=id).update(status="rejected")
    messages.success(request, "Charging station rejected")
    return redirect('/view_charging_station')


# -----------------------------
# CHARGING STATION PANEL
# -----------------------------

def home_charging_station(request):
    return render(request, "Charging Station/charging index.html")


def reg(request):
    return render(request, "Charging Station/charging station register.html")


@csrf_exempt
def reg_post(request):
    if request.method == "POST":
        # template uses textfield/textfield2/etc. for form fields
        name = request.POST.get('textfield')
        email = request.POST.get('textfield2')
        contact = request.POST.get('textfield3')
        place = request.POST.get('textfield4')
        latitude = request.POST.get('textfield5') or request.POST.get('textfield6')
        longitude = request.POST.get('textfield7') or request.POST.get('textfield7')
        password = request.POST.get('textfield6') or request.POST.get('textfield5')

        # Ensure we have a username/email and password
        if not email or not password:
            return HttpResponse("<script>alert('Please provide email and password');window.location='/reg'</script>")

        if Login.objects.filter(username=email).exists():
            return HttpResponse("<script>alert('User already exists');window.location='/reg'</script>")

        login_obj = Login.objects.create(username=email, password=password, usertype="chargingstation")

        # Store a charging station record (if the form is for charging stations)
        try:
            lat_val = float(latitude) if latitude else 0.0
        except Exception:
            lat_val = 0.0

        try:
            long_val = float(longitude) if longitude else 0.0
        except Exception:
            long_val = 0.0

        ChargingStation.objects.create(
            name=name or email,
            email=email,
            contact=contact or "",
            place=place or "",
            latitude=lat_val,
            longitude=long_val,
            login=login_obj,
        )

        return HttpResponse("<script>alert('Registered');window.location='/'</script>")

    return redirect('/')


def add_charge(request):
    return render(request, "Charging Station/add charge.html")


@csrf_exempt
def add_charge_post(request):
    fare = request.POST.get('textfield')
    if fare:
        try:
            fare_val = float(fare)
        except ValueError:
            return HttpResponse("<script>alert('Invalid fare');window.location='/view_charge'</script>")

        station = None
        lid = request.session.get('lid')
        if lid:
            station = ChargingStation.objects.filter(login_id=lid).first()

        if station:
            Charge.objects.create(fare=fare_val, charging_station=station)
            return HttpResponse("<script>alert('Charge added');window.location='/view_charge'</script>")

    return HttpResponse("<script>alert('Charge not added');window.location='/view_charge'</script>")


def view_charge(request):
    station = None
    lid = request.session.get('lid')
    if lid:
        station = ChargingStation.objects.filter(login_id=lid).first()

    if station:
        data = Charge.objects.filter(charging_station=station)
    else:
        data = Charge.objects.all()

    return render(request, "Charging Station/view charge.html", {"data": data})


def remove_charge(request, id):
    try:
        Charge.objects.filter(id=id).delete()
        return HttpResponse("<script>alert('Charge removed');window.location='/view_charge'</script>")
    except Exception:
        return HttpResponse("<script>alert('Error removing charge');window.location='/view_charge'</script>")


def edit_charge(request, id):
    charge = Charge.objects.get(id=id)
    return render(request, "Charging Station/edit charge.html", {"data": charge})


@csrf_exempt
def edit_charge_post(request, id):
    if request.method == "POST":
        fare = request.POST.get('textfield2')
        try:
            fare_val = float(fare)
        except (TypeError, ValueError):
            return HttpResponse("<script>alert('Invalid fare');window.location='/view_charge'</script>")

        # Update the Charge object
        Charge.objects.filter(id=id).update(fare=fare_val)
        return HttpResponse("<script>alert('Charge updated');window.location='/view_charge'</script>")
    return redirect('/view_charge')


# -----------------------------
# CHARGING SLOT MANAGEMENT
# -----------------------------

def add_charging_slot(request, id):
    return render(request, "Charging Station/add charging slot.html", {"id": id})


@csrf_exempt
def add_charging_slot_post(request, id):
    if request.method == "POST":
        slot_no = request.POST.get('slotno')
        if not slot_no:
            return HttpResponse("<script>alert('Slot number required');window.location='/add_charging_slot/%s'</script>" % id)
        try:
            time_slot = TimeSlot.objects.get(id=id)
            ChargingSlot.objects.create(slot_no=slot_no, status='available', time_slot=time_slot)
            return HttpResponse("<script>alert('Slot Added');window.location='/view_charging_slot/%s'</script>" % id)
        except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/add_charging_slot/{id}'</script>")
    return redirect(f'/add_charging_slot/{id}')


def edit_charging_slot(request, id):
    slot = ChargingSlot.objects.get(id=id)
    return render(request, "Charging Station/edit charging slot.html", {"data": slot})


@csrf_exempt
def edit_charging_slot_post(request, id):
    if request.method == "POST":
        slot_no = request.POST.get('slotno')
        status = request.POST.get('status')
        try:
            slot = ChargingSlot.objects.get(id=id)
            if slot_no:
                slot.slot_no = slot_no
            if status:
                slot.status = status
            slot.save()
            return HttpResponse(f"<script>alert('Slot Updated');window.location='/view_charging_slot/{slot.time_slot_id}'</script>")
        except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/edit_charging_slot/{id}'</script>")
    return redirect(f'/edit_charging_slot/{id}')


def delete_charging_slot(request, id):
    try:
        slot = ChargingSlot.objects.get(id=id)
        time_slot_id = slot.time_slot_id
        slot.delete()
        return HttpResponse(f"<script>alert('Slot Deleted');window.location='/view_charging_slot/{time_slot_id}'</script>")
    except Exception:
        return HttpResponse("<script>alert('Error deleting slot');window.location='/view_charge'</script>")


# -----------------------------
# TIME SLOT
# -----------------------------

def add_time_slot(request):
    return render(request, "Charging Station/add time slot.html")


@csrf_exempt
def add_time_slot_post(request):
    if request.method == "POST":
        total_slot = request.POST.get('textfield')
        date = request.POST.get('textfield2')
        start_time = request.POST.get('textfield3')
        end_time = request.POST.get('textfield4')

        # Get the charging station for the logged-in user
        lid = request.session.get('lid')
        station = None
        if lid:
            station = ChargingStation.objects.filter(login_id=lid).first()

        if not (total_slot and date and start_time and end_time and station):
            return HttpResponse("<script>alert('All fields required or not logged in as station');window.location='/add_time_slot'</script>")

        try:
            TimeSlot.objects.create(
                date=date,
                start_time=start_time,
                end_time=end_time,
                total_slot=total_slot,
                charging_station=station
            )
            return HttpResponse("<script>alert('Time slot added');window.location='/view_time_slot'</script>")
        except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/add_time_slot'</script>")
    return redirect('/add_time_slot')


def view_time_slot(request):
    # Show only time slots for the logged-in charging station
    lid = request.session.get('lid')
    station = None
    if lid:
        station = ChargingStation.objects.filter(login_id=lid).first()
    if station:
        data = TimeSlot.objects.filter(charging_station=station)
    else:
        data = TimeSlot.objects.none()
    return render(request, "Charging Station/view time slot.html", {"data": data})


def remove_time_slot(request, id):
    try:
        TimeSlot.objects.filter(id=id).delete()
        return HttpResponse("<script>alert('Time slot removed');window.location='/view_time_slot'</script>")
    except Exception:
        return HttpResponse("<script>alert('Error removing time slot');window.location='/view_time_slot'</script>")


def edit_time_slot(request, id):
    timeslot = TimeSlot.objects.get(id=id)
    return render(request, "Charging Station/edit time slot.html", {"data": timeslot})


@csrf_exempt
def edit_time_slot_post(request, id):
    if request.method == "POST":
        total_slot = request.POST.get('textfield')
        date = request.POST.get('textfield2')
        start_time = request.POST.get('textfield3')
        end_time = request.POST.get('textfield4')

        try:
            TimeSlot.objects.filter(id=id).update(
                total_slot=total_slot,
                date=date,
                start_time=start_time,
                end_time=end_time
            )
            return HttpResponse("<script>alert('Time slot updated');window.location='/view_time_slot'</script>")
        except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/edit_time_slot/{id}'</script>")
    return redirect('/view_time_slot')


# -----------------------------
# BOOKINGS
# -----------------------------

def view_booking(request):
    return render(request, "Charging Station/view booking.html")


def view_available_slot(request):
    return render(request, "Charging Station/view available slot.html")


def view_charging_slot(request, id):
    slots = ChargingSlot.objects.filter(time_slot_id=id)
    return render(request, "Charging Station/view charging slot.html", {"data": slots})


# -----------------------------
# PROFILE
# -----------------------------

def view_profile(request):
    return render(request, "Charging Station/view profile.html")


def view_rating(request):
    return render(request, "Charging Station/view rating.html")


# -----------------------------
# PAYMENT
# -----------------------------

from django.shortcuts import get_object_or_404


def charging_station_view_payment(request):
    user = User.objects.filter(login_id=request.session.get('lid')).first()
    payments = Payment.objects.none()
    month = None
    year = None

    if user:
        payments = Payment.objects.filter(booking__user=user).select_related(
            'booking__charging_slot__time_slot__charging_station'
        )

        if request.method == 'POST':
            month = request.POST.get('month')
            year = request.POST.get('year')
            if month and year:
                try:
                    month_num = datetime.datetime.strptime(month, "%B").month
                    payments = payments.filter(date__year=int(year), date__month=month_num)
                except Exception:
                    pass

    return render(request, "Charging Station/view payment history.html", {
        "payments": payments,
        "month": month,
        "year": year,
    })


def payment_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    booking = payment.booking
    user = booking.user
    slot = booking.charging_slot
    station = slot.time_slot.charging_station
    receipt_id = f"RCPT{payment.id:06d}"

    auto_download = request.GET.get('download', '0') in ['1', 'true', 'yes']

    return render(request, "Charging Station/payment_receipt.html", {
        "receipt_id": receipt_id,
        "user": user,
        "station": station,
        "slot": slot,
        "booking": booking,
        "amount": payment.amount,
        "auto_download": auto_download,
    })


# -----------------------------
# ANDROID API (Dummy)
# -----------------------------

def and_login(request): return JsonResponse({"status": "ok"})
def and_reset_password(request): return JsonResponse({"status": "ok"})
def and_user_register(request): return JsonResponse({"status": "ok"})
def and_send_complaint(request): return JsonResponse({"status": "ok"})
def and_send_rating(request): return JsonResponse({"status": "ok"})
def and_view_available_slot(request): return JsonResponse({"status": "ok"})
def and_view_charging_slot(request): return JsonResponse({"status": "ok"})
def and_view_reply(request): return JsonResponse({"status": "ok"})
def and_view_nearby_charging_station(request): return JsonResponse({"status": "ok"})
def and_view_previous_booking(request): return JsonResponse({"status": "ok"})
def and_view_profile(request): return JsonResponse({"status": "ok"})
def and_view_available_timeslot(request): return JsonResponse({"status": "ok"})
def and_offline_payment(request): return JsonResponse({"status": "ok"})
def android_online_payment(request): return JsonResponse({"status": "ok"})
def and_view_slot_with_date(request): return JsonResponse({"status": "ok"})
