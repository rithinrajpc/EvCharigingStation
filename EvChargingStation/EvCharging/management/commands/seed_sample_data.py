import random
import datetime

from django.core.management.base import BaseCommand

from EvCharging.models import ChargingStation, Login, TimeSlot, ChargingSlot


class Command(BaseCommand):
    help = "Seed the database with sample charging station, timeslot, and slot data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample data...")

        # Create admin login if not exists
        admin_login, _ = Login.objects.get_or_create(
            username="admin",
            defaults={
                "password": "admin123",
                "usertype": "admin",
            },
        )

        sample_stations = [
            {"name": "GreenCharge Hub", "email": "green@charge.com", "contact": "+911234567890", "place": "Kochi", "status": "approved"},
            {"name": "FastVolt Station", "email": "fastvolt@charge.com", "contact": "+919876543210", "place": "Trivandrum", "status": "approved"},
            {"name": "EcoCharge Point", "email": "eco@charge.com", "contact": "+919112233445", "place": "Bengaluru", "status": "rejected"},
            {"name": "PowerStop Depot", "email": "power@stop.com", "contact": "+919998887776", "place": "Mumbai", "status": "approved"},
            {"name": "ChargeWave Center", "email": "wave@charge.com", "contact": "+919223344556", "place": "Chennai", "status": "rejected"},
        ]

        for station_data in sample_stations:
            login, _ = Login.objects.get_or_create(
                username=station_data["email"],
                defaults={
                    "password": "station123",
                    "usertype": "chargingstation",
                },
            )

            station, created = ChargingStation.objects.get_or_create(
                email=station_data["email"],
                defaults={
                    "name": station_data["name"],
                    "contact": station_data["contact"],
                    "place": station_data["place"],
                    "latitude": random.uniform(8.0, 12.0),
                    "longitude": random.uniform(75.0, 77.0),
                    "status": station_data["status"],
                    "login": login,
                },
            )

            if created:
                self.stdout.write(f"Created station: {station.name} ({station.status})")

            # Create a time slot and charging slots for each station
            timeslot_date = datetime.date.today() + datetime.timedelta(days=random.randint(0, 14))
            timeslot = TimeSlot.objects.create(
                date=timeslot_date,
                start_time=datetime.time(hour=9, minute=0),
                end_time=datetime.time(hour=18, minute=0),
                total_slot=5,
                charging_station=station,
            )
            self.stdout.write(f"  Added time slot for {station.name} on {timeslot.date}")

            for slot_num in range(1, 6):
                status = random.choice(["available", "booked", "maintenance"])
                ChargingSlot.objects.create(
                    slot_no=f"SLOT-{slot_num}",
                    status=status,
                    time_slot=timeslot,
                )

        self.stdout.write(self.style.SUCCESS("Sample data seeding complete."))
