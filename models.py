from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from main import Base


class Passenger(Base):
    __tablename__ = 'passenger'
    id = Column(Integer(), primary_key=True)
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    phone = Column(String(45), nullable=False)
    passwortNumber = Column(Integer(), nullable=False)
    passwortSeries = Column(String(5), nullable=False)
    password = Column(Integer, nullable=False)  # додано для ідентифікації
    username = Column(String(45), nullable=False)  # додано для ідентифікації
    address = Column(String(45), nullable=False)
    RentalService_serviceId = Column(Integer, ForeignKey('rentalService.serviceId'))
    rentalService = relationship("RentalService", secondary=type, backref="passenger")

class Administrator(Base):
    __tablename__ = 'administrator'
    idAdministrator = Column(Integer(), primary_key=True)
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    age = Column(Integer(), nullable=False)
    experience = Column(Integer(), nullable=False)
    email = Column(String(45), nullable=False)
    phone = Column(String(45), nullable=False)
    RentalService_serviceId = Column(Integer, ForeignKey('rentalService.serviceId'))
    rentalService = relationship("RentalService", secondary=type, backref="administrator")


class RentalService(Base):
    __tablename__ = 'rentalService'
    serviceId = Column(Integer(), primary_key=True)
    name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    phone = Column(String(45), nullable=False)
    websiteLink = Column(String(45), nullable=False)
    address = Column(String(45), nullable=False)


class Car(Base):
    __tablename__ = 'car'
    carId = Column(Integer(), primary_key=True)
    brand = Column(String(45), nullable=False)
    model = Column(String(45), nullable=False)
    maxSpeed = Column(Integer(), nullable=False)
    yearProduction = Column(Integer(), nullable=False)
    fuelConsumption = Column(Integer(), nullable=False)
    seatsNumber = Column(Integer(), nullable=False)
    status = Column(String(45), nullable=False)
    Reservation_reservId = Column(Integer, ForeignKey('reservation.reservId'))
    reservation = relationship("Reservation", secondary=type, backref="car")
    RentalService_serviceId = Column(Integer, ForeignKey('rentalService.serviceId'))
    rentalService = relationship("RentalService", secondary=type, backref="car")


class Reservation(Base):
    __tablename__ = 'reservation'
    reservId = Column(Integer(), primary_key=True)
    startTime = Column(DateTime(), default=datetime)
    endTime = Column(DateTime(), default=datetime)