from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from models import *
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt as bcrypt
from sqlalchemy import *
from flask import *
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import *
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import and_
app = Flask(__name__)


#if __name__ == '__main__':

    # Підключаємось до бази даних
engine = create_engine("mysql+pymysql://root:mira0369B@localhost:3306/mydb02")
    # з'єднуємось з базою даних
    #engine.connect()
metadata = MetaData()
Base = declarative_base(metadata=metadata)
session = sessionmaker(bind=engine)
s = session()

ma = Marshmallow(app)

#SwaggerUrL
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL,
    config={'app_name': 'Event Tickets API'})   #поміняти назву
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

auth = HTTPBasicAuth()

@auth.verify_password      #автентифікація пасажира
def verify_password(username, password):
    try:
        user = s.query(User).filter(and_(User.username == username,
                                         User.password == password)).first() is not None
        if user:
            return username
    except:
        return Response(status=500)

@auth.get_user_roles
def get_user_roles(username):
    user = s.query(User).filter(User.username == username).first()
    return user.Role

# для відловлення помилок при автентифікації
@app.errorhandler(401)
def handle_401_error(_error):
    return make_response(jsonify({'error': 'Unauthorised'}), 401)

@app.errorhandler(403)
def handle_403_error(_error):
    return make_response(jsonify({'error': 'Forbidden'}), 403)

@app.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({'error': 'Server error'}), 500)

class CarSchema(ma.Schema):
    class Meta:
        fields = ('carId', 'brand', 'model', 'maxSpeed', 'yearProduction',
                  'fuelConsumption', 'seatsNumber', 'status', 'RentalService_serviceId')

Car_schema = CarSchema(many=False)
Cars_schema = CarSchema(many=True)


class RentalServiceSchema(ma.Schema):
    class Meta:
        fields = ('serviceId', 'name', 'email', 'phone',
                  'websiteLink', 'address')


RentalService_schema = RentalServiceSchema(many=False)
RentalServices_schema = RentalServiceSchema(many=True)

#Формування відповіді на запити(лінки)
#Отримати інформацію про машину по ID
@app.route("/Car/<int:carId>", methods=["GET"])
def getCarById(carId):
    car = s.query(Car).filter(Car.carId == carId).one()
    return Car_schema.jsonify(car)

# отримати список усіх машин сервісу по ID(сервісу)
@app.route("/Car/get-by-service-id/<int:RentalService_serviceId>", methods=["GET"])
def getCarsByServiceId(RentalService_serviceId):
    cars = s.query(Car).filter(Car.RentalService_serviceId == RentalService_serviceId).all()
    return Car_schema.jsonify(cars)

#додавання однієї машини, може додати тільки SuperUser
@app.route("/Car", methods=["POST"])
@auth.login_required(role=['SuperUser'])
def addCar():
    try:
        carId = request.json['carId']
        brand = request.json['brand']
        model = request.json['model']
        maxSpeed = request.json['maxSpeed']
        yearProduction = request.json['yearProduction']
        fuelConsumption = request.json['fuelConsumption']
        seatsNumber = request.json['seatsNumber']
        status = request.json['status']
        RentalService_serviceId = request.json['serviceId']
        service = s.query(RentalService).filter(RentalService.serviceId == RentalService_serviceId).one()
        Username = service.Username
        current = auth.username()
        if current != Username:
            return Response(status=403, response='Access denied')
        new_car = Car(CarId=carId,  brand=brand,
                            model=model, maxSpeed=maxSpeed, yearProduction=yearProduction,
                            fuelConsumption=fuelConsumption, seatsNumber=seatsNumber, status=status)

        s.add(new_car)
        s.commit()
        return Car_schema.jsonify(new_car)

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})


#редагування машини по ID
@app.route("/Car/<int:carId>", methods=["PUT"])
@auth.login_required(role=['SuperUser'])
def updateCar(carId):
    car = s.query(Car).filter(Car.carId == carId).one()
    Username = car.Username
    current = auth.username()
    if current != Username:
        return Response(status=405, response='Access denied')
    try:
        carId = request.json['carId']
        brand = request.json['brand']
        model = request.json['model']
        maxSpeed = request.json['maxSpeed']
        yearProduction = request.json['yearProduction']
        fuelConsumption = request.json['fuelConsumption']
        seatsNumber = request.json['seatsNumber']
        status = request.json['status']
        RentalService_serviceId = request.json['serviceId']

        car.carId = carId
        car.brand = brand
        car.model = model
        car.maxSpeed = maxSpeed
        car.yearProduction = yearProduction
        car.fuelConsumption = fuelConsumption
        car.seatsNumber = seatsNumber
        car.status = status
        car.RentalService_serviceId = RentalService_serviceId

        s.commit()

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

    return Car_schema.jsonify(car)

#видалення машини по ID
@app.route("/car/<int:carId>", methods=["DELETE"])
@auth.login_required(role=['SuperUser'])
def deleteCarById(carId):
    car = s.query(Car).filter(Car.carId == carId).one()
    Username = Car.Username
    current = auth.username()
    if current != Username:
        return Response(status=403, response='Access denied')
    s.delete(car)
    s.commit()
    return jsonify({"Success": "Event deleted."})

#видалення машин по ID сервісу
@app.route("/Car/<int:RentalService_serviceId>", methods=["DELETE"])
@auth.login_required(role=['SuperUser'])
def deleteCarsByEventId(RentalService_serviceId):
    event = s.query(RentalService).filter(RentalService.serviceId == RentalService_serviceId).one()
    Username = event.Username
    current = auth.username()
    if current != Username:
        return Response(status=403, response='Access denied')
    cars = s.query(Car).filter(Car.RentalService_serviceId == RentalService_serviceId).all()

    for car in cars:
        s.delete(car)

    s.commit()
    return jsonify({"Success": "Cars deleted."})

#додавання нового сервісу
@app.route("/RentalService", methods=["POST"])
@auth.login_required(role=['SuperUser'])
def addRentalService():
    try:
        serviceId = request.json['serviceId']
        name = request.json['name']
        email = request.json['name']
        phone = request.json['phone']
        websiteLink = request.json['websiteLink']
        address = request.json['address']

        new_service = RentalService(serviceId=serviceId,
                        name = name, email=email,
                        phone=phone, websiteLink=websiteLink,
                        address = address, Username=auth.username())

        s.add(new_service)
        s.commit()
        return RentalService_schema.jsonify(new_service)

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

#видалення сервісу по ID
@app.route("/RentalService/<int:serviceId>", methods=["DELETE"])
@auth.login_required(role=['SuperUser'])
def deleteRentalServiceById(serviceId):
    service = s.query(RentalService).filter(RentalService.serviceId == serviceId).one()
    Username = RentalService.Username
    current = auth.username()
    if current != Username:
        return Response(status=403, response='Access denied')
    s.delete(service)
    s.commit()
    return jsonify({"Success": "Event deleted."})

#редагувати сервіс по ID
@app.route("/RentalService/<int:serviceId>", methods=["PUT"])
@auth.login_required(role=['SuperUser'])
def updateServiceById(serviceId):
    service = s.query(RentalService).filter(RentalService.serviceId == serviceId).one()
    Username = RentalService.Username
    current = auth.username()
    if current != Username:
        return Response(status=405, response='Access denied')
    try:

        serviceId = request.json['serviceId']
        name = request.json['name']
        email = request.json['name']
        phone = request.json['phone']
        websiteLink = request.json['websiteLink']
        address = request.json['address']


        service.serviceId = serviceId
        service.name = name
        service.email = email
        service.phone = phone
        service.websiteLink = websiteLink
        service.address = address


        s.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})

    return RentalService_schema.jsonify(service)

#Passenger and Admin--------------------------------------------

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'phone', 'passwortNumber',
                  'passwortSeries', 'password', 'username',
                  'RentalService_serviceId', 'Role')


User_schema = UserSchema(many=False)
Users_schema = UserSchema(many=True)

# отримати всі машини одного користувача
@app.route("/Car/get-by-userid/<string:username>", methods=["GET"])
@auth.login_required(role=['User'])
def getUsersCars(username):
    current = auth.username()
    if current != username:
        return Response(status=403, response='Access denied')
    cars = s.query(Car).filter(Car.username == username).all()

    return Cars_schema.jsonify(cars)

#додати нового користувача (клієнт)
@app.route("/User", methods=["POST"])
def addUser():
    try:
        id = request.json['id']
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        phone = request.json['phone']
        passwortNumber = request.json['passwortNumber']
        passwortSeries = request.json['passwortSeries']
        username = request.json['username']
        password = request.json['password']
        RentalService_serviceId = request.json['RentalService_serviceId']
        # password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        new_user = User(id=id, firstName=firstName, lastName=lastName,
                        phone=phone, passwortNumber=passwortNumber,
                        passwortSeries=passwortSeries,
                        username = username,
                        password=password, Role="User",
                        RentalService_serviceId = RentalService_serviceId)

        s.add(new_user)
        s.commit()
        return User_schema.jsonify(new_user)

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})


#додати нового користувача (адмін)
@app.route("/Admin", methods=["POST"])
def addAdmin():
    try:
        id = request.json['id']
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        phone = request.json['phone']
        passwortNumber = request.json['passwortNumber']
        passwortSeries = request.json['passwortSeries']
        username = request.json['username']
        password = request.json['password']
        RentalService_serviceId = request.json['RentalService_serviceId']
        # password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        new_user = User(id=id, firstName=firstName, lastName=lastName,
                        phone=phone, passwortNumber=passwortNumber,
                        passwortSeries=passwortSeries,
                        username = username,
                        password=password, Role="Admin",
                        RentalService_serviceId = RentalService_serviceId)

        s.add(new_user)
        s.commit()
        return User_schema.jsonify(new_user)

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

#орендування машини по ID
@app.route("/User/Reservation", methods=["PUT"])
@auth.login_required(role=['User'])
def ReservationCarById():

    try:

        carId = request.json['carId']
        username = request.json['username']
        status = request.json['status']
        current = auth.username()
        if current != username:
            return Response(status=403, response='Access denied')
        car = s.query(Car).filter(Car.carId == carId).one()

        if (car.status==1):
            return handle_403_error(1)

        if (car.status==0):
            if car.username != username:
                return handle_403_error(1)

            if status == 0:
                car.username = None

            car.status = status

        else:
            if status == 0:
                return Car_schema.jsonify(car)

            car.status = status
            car.username = username

        s.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})

    return Car_schema.jsonify(car)



# class Passenger(Base):
#     __tablename__ = 'passenger'
#     id = Column(Integer(), primary_key=True)
#     firstName = Column(String(45), nullable=False)
#     lastName = Column(String(45), nullable=False)
#     #email = Column(String(45), nullable=False)
#     phone = Column(String(45), nullable=False)
#     passwortNumber = Column(Integer(), nullable=False)
#     passwortSeries = Column(String(5), nullable=False)
#     address = Column(String(45), nullable=False)
#     RentalService_serviceId = Column(Integer, ForeignKey('rentalService.serviceId'))
#     rentalService = relationship("RentalService", secondary=type, backref="passenger")
#
# class Administrator(Base):
#     __tablename__ = 'administrator'
#     idAdministrator = Column(Integer(), primary_key=True)
#     firstName = Column(String(45), nullable=False)
#     lastName = Column(String(45), nullable=False)
#     age = Column(Integer(), nullable=False)
#     experience = Column(Integer(), nullable=False)
#     email = Column(String(45), nullable=False)
#     phone = Column(String(45), nullable=False)
#     RentalService_serviceId = Column(Integer, ForeignKey('rentalService.serviceId'))
#     rentalService = relationship("RentalService", secondary=type, backref="administrator")
#
#
# class RentalService(Base):
#     __tablename__ = 'rentalService'
#     serviceId = Column(Integer(), primary_key=True)
#     name = Column(String(45), nullable=False)
#     email = Column(String(45), nullable=False)
#     phone = Column(String(45), nullable=False)
#     websiteLink = Column(String(45), nullable=False)
#     address = Column(String(45), nullable=False)
#
#
# class Car(Base):
#     __tablename__ = 'car'
#     carId = Column(Integer(), primary_key=True)
#     brand = Column(String(45), nullable=False)
#     model = Column(String(45), nullable=False)
#     maxSpeed = Column(Integer(), nullable=False)
#     yearProduction = Column(Integer(), nullable=False)
#     fuelConsumption = Column(Integer(), nullable=False)
#     seatsNumber = Column(Integer(), nullable=False)
#     status = Column(String(45), nullable=False)
#     #Reservation_reservId = Column(Integer, ForeignKey('reservation.reservId'))
#     #reservation = relationship("Reservation", secondary=type, backref="car")
#     RentalService_serviceId = Column(Integer, ForeignKey('rentalService.serviceId'))
#     rentalService = relationship("RentalService", secondary=type, backref="car")
#
#
# ####class Reservation(Base):
#     __tablename__ = 'reservation'
#     reservId = Column(Integer(), primary_key=True)
#     startTime = Column(DateTime(), default=datetime)
#     endTime = Column(DateTime(), default=datetime)


    #Base.metadata.create_all(engine)
    #Base.metadata.drop_all(engine)

    #print(engine)