import os
import random
import datetime

# Configure the settings for the project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chore_tracker.settings")

# Setup and configure the project settings
import django
from django.utils import timezone
django.setup()

# FAKE POP SCRIPT
from chores.models import Chore, ChoreInterval, ChoreInstance
from chores.views import generate_instances
from faker import Faker

fake_generator = Faker()


def populate(n=5):
    for chore in range(n):

        # Create the fake data for that entry
        fake_chore_name = fake_generator.bs()
        fake_description = fake_generator.text(random.randint(20, 500))
        fake_repeats = random.randint(0, 1)
        fake_datetime = fake_generator.date_time_between(
            start_date=datetime.datetime.now(),
            end_date=(datetime.datetime.now(
                tz=timezone.get_default_timezone()) + datetime.timedelta(days=10)),
            tzinfo=timezone.get_default_timezone()
        )

        fake_datetime.replace(tzinfo=timezone.utc)

        # Create new WebPage entry
        new_chore = Chore.objects.get_or_create(
            name=fake_chore_name,
            description=fake_description,
            repeats=fake_repeats,
            datetime=fake_datetime
        )[0]

        new_chore_interval = None
        if fake_repeats:
            fake_interval = random.choice(ChoreInterval.IntervalChoice.choices)[0]

            fake_custom_interval = None
            if fake_interval == ChoreInterval.IntervalChoice.CUSTOM:
                fake_custom_interval = random.randint(2, 17)

            new_chore_interval = ChoreInterval.objects.get_or_create(
                chore=new_chore,
                repeat_interval=fake_interval,
                repeat_custom_interval=fake_custom_interval
            )[0]

        ChoreInstance.objects.bulk_create(generate_instances(new_chore, new_chore_interval))


if __name__ == '__main__':
    print("Populating scripts!")
    populate(20)
    print("Populating complete")
