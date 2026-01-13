import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_vote.settings')
django.setup()

from core.models import CustomUser
users = CustomUser.objects.all()
print(f"Total users: {users.count()}")
for u in users:
    print(f"User: {u.username}, Role: {u.role}, Approved: {u.is_approved}, Superuser: {u.is_superuser}")
