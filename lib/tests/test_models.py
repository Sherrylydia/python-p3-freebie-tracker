# lib/tests/test_models.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base, Dev, Company, Freebie

# Setup in-memory database fixture
@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_give_freebie_creates_freebie(session):
    dev = Dev(name="Alice")
    company = Company(name="Google", founding_year=1998)
    session.add_all([dev, company])
    session.commit()

    company.give_freebie(dev, "Sticker", 1, session)
    freebie = session.query(Freebie).first()

    assert freebie.item_name == "Sticker"
    assert freebie.dev == dev
    assert freebie.company == company

def test_dev_received_one(session):
    dev = Dev(name="Bob")
    company = Company(name="Meta", founding_year=2004)
    session.add_all([dev, company])
    session.commit()

    company.give_freebie(dev, "Mug", 5, session)
    assert dev.received_one("Mug") is True
    assert dev.received_one("Cap") is False

def test_dev_give_away(session):
    dev1 = Dev(name="Carol")
    dev2 = Dev(name="Dave")
    company = Company(name="Netflix", founding_year=1997)
    session.add_all([dev1, dev2, company])
    session.commit()

    company.give_freebie(dev1, "Pen", 2, session)
    freebie = dev1.received_freebies[0]
    dev1.give_away(dev2, freebie)

    assert freebie.dev == dev2

def test_freebie_print_details(session, capsys):
    dev = Dev(name="Eve")
    company = Company(name="Amazon", founding_year=1994)
    session.add_all([dev, company])
    session.commit()

    company.give_freebie(dev, "T-shirt", 10, session)
    freebie = session.query(Freebie).first()
    freebie.print_details()

    captured = capsys.readouterr()
    assert "Eve owns a T-shirt from Amazon" in captured.out

def test_oldest_company(session):
    c1 = Company(name="IBM", founding_year=1911)
    c2 = Company(name="Apple", founding_year=1976)
    c3 = Company(name="Dell", founding_year=1984)
    session.add_all([c1, c2, c3])
    session.commit()

    assert Company.oldest_company(session) == c1
