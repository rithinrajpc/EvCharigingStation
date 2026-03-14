from django.db import models


# -----------------------------
# LOGIN MODEL
# -----------------------------
class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)

    def __str__(self):
        return self.username


# -----------------------------
# CHARGING STATION
# -----------------------------
class ChargingStation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    place = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=50, default='pending')
    login = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# -----------------------------
# TIME SLOT
# -----------------------------
class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_slot = models.IntegerField()
    charging_station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.start_time}"


# -----------------------------
# CHARGE
# -----------------------------
class Charge(models.Model):
    fare = models.FloatField()
    charging_station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fare)


# -----------------------------
# CHARGING SLOT
# -----------------------------
class ChargingSlot(models.Model):
    slot_no = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return self.slot_no


# -----------------------------
# USER
# -----------------------------
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    place = models.CharField(max_length=100)
    land_mark = models.CharField(max_length=100)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# -----------------------------
# RATING
# -----------------------------
class Rating(models.Model):
    rate = models.CharField(max_length=10)
    date = models.DateField()
    charging_station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.rate


# -----------------------------
# COMPLAINT
# -----------------------------
class Complaint(models.Model):
    complaint = models.TextField()
    reply = models.TextField(blank=True)
    complaint_date = models.DateField()
    reply_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.complaint


# -----------------------------
# BOOKING
# -----------------------------
class Booking(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charging_slot = models.ForeignKey(ChargingSlot, on_delete=models.CASCADE)

    def __str__(self):
        return self.status


# -----------------------------
# PAYMENT
# -----------------------------
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return str(self.amount)
