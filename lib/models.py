# lib/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    received_freebies = relationship("Freebie", back_populates="dev")

    def received_one(self, item_name):
        return any(f.item_name == item_name for f in self.received_freebies)

    def give_away(self, other_dev, freebie):
        if freebie in self.received_freebies:
            freebie.dev = other_dev

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship("Freebie", back_populates="company")

    def give_freebie(self, dev, item_name, value, session):
        new_freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        session.add(new_freebie)
        session.commit()

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship("Dev", back_populates="received_freebies")
    company = relationship("Company", back_populates="freebies")

    def print_details(self):
        print(f"{self.dev.name} owns a {self.item_name} from {self.company.name}")
