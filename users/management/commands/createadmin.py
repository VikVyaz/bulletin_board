from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        u = get_user_model()
        if not get_user_model().objects.filter(email="admin@mail.com").exists():
            user = u.objects.create(
                username='test',
                first_name="test",
                last_name="test",
                phone="test",
                email="admin@mail.com",
                role="admin",
            )

            user.set_password("1234")

            user.is_active = True
            user.is_staff = True
            user.is_superuser = True

            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Создан тестовый admin '{user.email}', пароль 1234."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Тестовый админ существует.\n"
                    f"'{get_user_model().objects.filter(email='admin@mail.com')[0].email}', пароль 1234"
                )
            )
