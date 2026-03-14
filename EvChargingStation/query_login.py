from EvCharging.models import Login

print('Current Login Credentials:')
for obj in Login.objects.all():
    print('ID:', obj.id, 'Username:', obj.username, 'Password:', obj.password, 'Usertype:', obj.usertype)