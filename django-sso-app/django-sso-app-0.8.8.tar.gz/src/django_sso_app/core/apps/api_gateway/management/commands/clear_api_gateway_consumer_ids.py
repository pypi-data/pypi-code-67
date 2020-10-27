from django.core.management.base import BaseCommand  # , CommandError
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Sets apigw_consumer_id to "None"'

    def handle(self, *args, **options):
        users = User.objects.filter(is_staff=False, is_superuser=False)
        users_count = users.count()
        updated_users = 0

        for user in users:
            try:
                profile = user.sso_app_profile
                profile.apigw_consumer_id = None
                profile.save()

                updated_users += 1
                self.stdout.write(self.style.SUCCESS('{}/{}'.format(updated_users, users_count)))

            except Exception as e:
                self.stdout.write(self.style.ERROR('Error "{}" updating apigw_consumer_id for "{}"'.format(e, user)))

        self.stdout.write(self.style.SUCCESS('Updated {}/{} users'.format(updated_users, users_count)))
