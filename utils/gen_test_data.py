#!/usr/bin/env python
from faker import Factory
import json
fake = Factory.create('de_DE')
fake.seed(1239847)

people = []
for idx in range(50):
    name = fake.name()
    city = fake.city()
    email = fake.email()
    people.append((fake.name(), (city, email)))


total = {}
total['people'] = people
total['addresses'] = [fake.address() for x in range(50)]
total['text'] = '\n'.join([fake.text() for x in range(30)])
print(json.dumps(total, indent=2))
