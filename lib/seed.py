

from base import Base, engine, session
from company import Company
from dev import Dev
from freebie import Freebie

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

apple = Company(name="Apple", founding_year=1976)
google = Company(name="Google", founding_year=1998)


alice = Dev(name="Alice")
bob = Dev(name="Bob")

session.add_all([apple, google, alice, bob])
session.commit()

apple.give_freebie(alice, "Sticker", 5)
google.give_freebie(bob, "Tote Bag", 15)
apple.give_freebie(bob, "Water Bottle", 10)
