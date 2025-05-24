

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base, session
from freebie import Freebie

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship('Freebie', back_populates='company')

    @property
    def devs(self):
       
        return list({freebie.dev for freebie in self.freebies})

    ddef give_freebie(self, dev, item_name, value):
    from sqlalchemy.orm import object_session

    new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
    current_session = object_session(self)
    current_session.add(new_freebie)
    current_session.commit()


    @classmethod
    def oldest_company(cls):
        from base import session
        return session.query(cls).order_by(cls.founding_year).first()
