from sqlalchemy import Column, Integer, String, Date, func, select
from sqlalchemy.orm import relationship, foreign, column_property

from database import engine, Base
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import join


class SoftwareInstalledModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'software_installed'

    software_id = Column(Integer)
    computer_id = Column(Integer)
    s_installed_id = Column(Integer, primary_key=True)


class SoftwareModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'software'

    software_id = Column(Integer, primary_key=True)
    name = Column(String(75))
    description = Column(String(350))
    count = Column(Integer)
    expiration_date = Column(Date)
    type = Column(String(50))
    contact_id = Column(Integer)

    software_info = relationship(
        'SoftwareInstalledModel',
        primaryjoin=(software_id == foreign(SoftwareInstalledModel.software_id)),
        uselist=True, backref='software')

    # https://docs.sqlalchemy.org/en/13/orm/mapped_sql_expr.html#using-column-property
    count_connected = column_property(
        select([func.count(SoftwareInstalledModel.s_installed_id)])
        .where(SoftwareInstalledModel.software_id == software_id))


class PcieModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'pcie'

    pcie_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    producer = Column(String(100))
    type = Column(String(35))


class PcieInstalledModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'pcie_installed'

    pcie_id = Column(Integer)
    computer_id = Column(Integer)
    p_installed_id = Column(Integer, primary_key=True)
    pcie = relationship('PcieModel', primaryjoin=(pcie_id == foreign(PcieModel.pcie_id)),
                        uselist=False, backref='pcieInfo')


class ProcessorModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'processor'

    processor_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    producer = Column(String(100))
    clock = Column(String(10))
    architecture = Column(String(30))
    socket = Column(String(15))


class ProcessorInstalledModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'processor_installed'

    processor_id = Column(Integer)
    computer_id = Column(Integer)
    p_installed_id = Column(Integer, primary_key=True)
    processor = relationship('ProcessorModel', primaryjoin=(processor_id == foreign(ProcessorModel.processor_id)),
                             uselist=False, backref='cpuInfo')


class RamModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'ram'

    ram_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    producer = Column(String(100))
    standard = Column(String(10))
    frequency = Column(Integer)
    capacity = Column(Integer)


class RamInstalledModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'ram_installed'

    r_installed_id = Column(Integer, primary_key=True)
    ram_id = Column(Integer)
    computer_id = Column(Integer)
    ram = relationship('RamModel', primaryjoin=(ram_id == foreign(RamModel.ram_id)), uselist=False, backref='ramInfo')


class MacAddressModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'mac_adressen'

    mid = Column(Integer, primary_key=True)
    computer_id = Column(Integer)
    type = Column(String(100))
    mac_adresse = Column(String(100))


class ComputerModel(Base):
    __table_args__ = {'extend_existing': True, "schema": "rechner_db"}
    __tablename__ = 'computers'

    computer_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    edv = Column(String(6))
    user_id = Column(Integer)
    ip = Column(Integer)
    os_id = Column(Integer)
    type = Column(String(50))
    mainboard_id = Column(Integer)
    note = Column(String(300))
    borrowable = Column(String(7))
    storage = Column(String(250))
    room_id = Column(Integer)
    ram = relationship('RamInstalledModel', primaryjoin=(computer_id == foreign(RamInstalledModel.computer_id)),
                       uselist=True, backref='computer')
    processor = relationship('ProcessorInstalledModel',
                             primaryjoin=(computer_id == foreign(ProcessorInstalledModel.computer_id)),
                             uselist=True, backref='computer')
    pcie = relationship('PcieInstalledModel',
                        primaryjoin=(computer_id == foreign(PcieInstalledModel.computer_id)),
                        uselist=True, backref='computer')
    software = relationship('SoftwareInstalledModel',
                            primaryjoin=(computer_id == foreign(SoftwareInstalledModel.computer_id)),
                            uselist=True, backref='computer')
    macadresses = relationship('MacAddressModel',
                               primaryjoin=(computer_id == foreign(MacAddressModel.computer_id)),
                               uselist=True, backref='computer')


class UserModel(Base):
    __table_args__ = {'extend_existing': True, "schema": "rechner_db"}
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    passwd = Column(String(256))
    role = Column(String(30))
    computer = relationship('ComputerModel', primaryjoin=(user_id == foreign(ComputerModel.user_id)), uselist=True,
                            backref='user')
    contact = relationship('SoftwareModel', primaryjoin=(user_id == foreign(SoftwareModel.contact_id)), uselist=True,
                           backref='contact')


class RoomModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'room'

    room_id = Column(Integer, primary_key=True)
    name = Column(String(75))
    etage = Column(String(10))
    description = Column(String(350))
    computer = relationship('ComputerModel',
                            primaryjoin=(room_id == foreign(ComputerModel.room_id)),
                            uselist=True,
                            backref='room')


class OSModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'operatingsystem'

    os_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    version = Column(String(20))
    computer = relationship('ComputerModel', primaryjoin=(os_id == foreign(ComputerModel.os_id)), uselist=True,
                            backref='os')


class MainboardModel(Base):
    __table_args__ = {"schema": "rechner_db"}
    __tablename__ = 'mainboard'

    mainboard_id = Column(Integer, primary_key=True)
    producer = Column(String(100))
    name = Column(String(100))
    socket = Column(String(15))
    sockets = Column(Integer)
    chipset = Column(String(25))
    dimmslots = Column(Integer)
    pcieslots = Column(Integer)
    m2slots = Column(Integer)
    sataconnectors = Column(Integer)
    formfactor = Column(String(15))
    ddr = Column(String(10))
    computer = relationship('ComputerModel', primaryjoin=(mainboard_id == foreign(ComputerModel.mainboard_id)),
                            uselist=True,
                            backref='mainboard')


print("Hello from models.py")
Base.prepare(engine)
