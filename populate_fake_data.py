import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backlog_tracker.settings')


import django
django.setup()

import random
from faker import Faker
from backlog_tracker_app.models import Movie, PersonalUser


fakegen = Faker()


def populate(N=5):
    for entry in range(N):
        #populate fake movies 
        fake_name = fakegen.name()
        fake_date = fakegen.date()
        fake_duration = random.randint(100, 200)

        fake_movie = Movie.objects.get_or_create(
            name=fake_name, release_date=fake_date, duration=fake_duration)[0]

        #populate fake users 
        fake_first_name = fakegen.first_name() 
        fake_last_name = fakegen.last_name() 
        fake_email = fakegen.company_email()

        fake_user = PersonalUser.objects.get_or_create(
            first_name=fake_first_name, last_name=fake_last_name, email=fake_email)[0]
    

if __name__ == '__main__':
    print('Populating data...')
    populate(10)
    print('Population script complete!')
