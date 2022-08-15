import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import *
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

ALL_OPERATIONS = ['eq', 'ne', 'like', 'ilike', 'is_null', 'in', 'not_in', 'lt', 'lte', 'gt', 'gte', 'range']

class Computer(SQLAlchemyObjectType):
    class Meta:
        model = ComputerModel
        interfaces = (graphene.relay.Node,)


class Room(SQLAlchemyObjectType):
    class Meta:
        model = RoomModel
        interfaces = (graphene.relay.Node,)


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)


class OS(SQLAlchemyObjectType):
    class Meta:
        model = OSModel
        interfaces = (graphene.relay.Node,)


class Mainboard(SQLAlchemyObjectType):
    class Meta:
        model = MainboardModel
        interfaces = (graphene.relay.Node,)


class Ram(SQLAlchemyObjectType):
    class Meta:
        model = RamModel
        interfaces = (graphene.relay.Node,)


class InstRam(SQLAlchemyObjectType):
    class Meta:
        model = RamInstalledModel
        interfaces = (graphene.relay.Node,)


class Processor(SQLAlchemyObjectType):
    class Meta:
        model = ProcessorModel
        interfaces = (graphene.relay.Node,)


class InstProcessor(SQLAlchemyObjectType):
    class Meta:
        model = ProcessorInstalledModel
        interfaces = (graphene.relay.Node,)


class Pcie(SQLAlchemyObjectType):
    class Meta:
        model = PcieModel
        interfaces = (graphene.relay.Node,)


class InstPcie(SQLAlchemyObjectType):
    class Meta:
        model = PcieInstalledModel
        interfaces = (graphene.relay.Node,)


class Software(SQLAlchemyObjectType):
    class Meta:
        model = SoftwareModel
        interfaces = (graphene.relay.Node,)


class InstSoftware(SQLAlchemyObjectType):
    class Meta:
        model = SoftwareInstalledModel
        interfaces = (graphene.relay.Node,)


class MacAddress(SQLAlchemyObjectType):
    class Meta:
        model = MacAddressModel
        interfaces = (graphene.relay.Node,)

class MacAddressFilter(FilterSet):
    class Meta:
        model = MacAddressModel
        fields = {
            'computer_id': ALL_OPERATIONS,
            'type': ALL_OPERATIONS,
            'mac_adresse': ALL_OPERATIONS,
        }

class ProcessorFilter(FilterSet):
    class Meta:
        model = ProcessorModel
        fields = {
            'name': ALL_OPERATIONS,
            'producer': ALL_OPERATIONS,
            'clock': ALL_OPERATIONS,
            'architecture': ALL_OPERATIONS,
            'socket': ALL_OPERATIONS,
        }


class RamFilter(FilterSet):
    class Meta:
        model = RamModel
        fields = {
            'name': ALL_OPERATIONS,
            'producer': ALL_OPERATIONS,
            'standard': ALL_OPERATIONS,
            'frequency': ALL_OPERATIONS,
            'capacity': ALL_OPERATIONS,
        }

class ComputerFilter(FilterSet):
    class Meta:
        model = ComputerModel
        fields = {
            'name': ALL_OPERATIONS,
            'edv': ALL_OPERATIONS,
            'computer_id': ALL_OPERATIONS,
            'room_id': ALL_OPERATIONS,
            'user_id': ALL_OPERATIONS,
            'ip': ALL_OPERATIONS,
            'os_id': ALL_OPERATIONS,
            'type': ALL_OPERATIONS,
            'mainboard_id': ALL_OPERATIONS,
            'note': ALL_OPERATIONS,
            'borrowable': ALL_OPERATIONS,
            'storage': ALL_OPERATIONS
        }

class UserFilter(FilterSet):
    class Meta:
        model = UserModel
        fields = {
            'user_id': ALL_OPERATIONS,
            'email': ALL_OPERATIONS,
            'firstname': ALL_OPERATIONS,
            'lastname': ALL_OPERATIONS,
            'role': ALL_OPERATIONS
        }

class SoftwareFilter(FilterSet):
    class Meta:
        model = SoftwareModel
        fields = {
            'computer_id': ALL_OPERATIONS
        }


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    room = graphene.Field(lambda: Room, room_id=graphene.Int())
    all_rooms = SQLAlchemyConnectionField(Room)

    user = graphene.Field(lambda: User, user_id=graphene.Int())
    all_users = SQLAlchemyConnectionField(User)
    all_users_with = FilterableConnectionField(connection=User, filters=UserFilter())

    computer = graphene.Field(lambda: Computer, computer_id=graphene.Int())
    all_Computers = FilterableConnectionField(connection=Computer, filters=ComputerFilter())

    os = graphene.Field(lambda: OS, os_id=graphene.Int())
    all_OSs = SQLAlchemyConnectionField(OS)

    mainboard = graphene.Field(lambda: Mainboard, mainboard_id=graphene.Int())
    all_Mainboards = SQLAlchemyConnectionField(Mainboard)

    ram = graphene.Field(lambda: Ram, ram_id=graphene.Int())
    all_Rams = FilterableConnectionField(connection=Ram, filters=RamFilter())

    instRam = graphene.Field(lambda: InstRam, computer_id=graphene.Int())
    all_instRam = SQLAlchemyConnectionField(InstRam)

    processor = graphene.Field(lambda: Processor, processor_id=graphene.Int())
    all_Processors = FilterableConnectionField(connection=Processor, filters=ProcessorFilter())

    instProcessor = graphene.Field(lambda: InstProcessor, computer_id=graphene.Int())
    all_instProcessor = SQLAlchemyConnectionField(InstProcessor)

    pcie = graphene.Field(lambda: Pcie, pcie_id=graphene.Int())
    all_Pcies = SQLAlchemyConnectionField(Pcie)

    instPcie = graphene.Field(lambda: InstPcie, computer=graphene.Int())
    all_instPcie = SQLAlchemyConnectionField(InstPcie)

    software = graphene.Field(lambda: Software, software_id=graphene.Int())
    all_Softwares = FilterableConnectionField(connection=Software, filters=SoftwareFilter())

    instSoftware = graphene.Field(lambda: InstSoftware, computer_id=graphene.Int())
    all_instSoftware = SQLAlchemyConnectionField(InstSoftware)

    mac_adress = graphene.Field(lambda : MacAddress, computer_id=graphene.Int())
    all_mac_adress = FilterableConnectionField(connection=MacAddress, filters=MacAddressFilter())

    def resolve_room(self, info, **kwargs):
        query = Room.get_query(info)
        room_id = kwargs.get('room_id')
        return query.filter(RoomModel.room_id == room_id).first()

    def resolve_user(self, info, **kwargs):
        query = User.get_query(info)
        user_id = kwargs.get('user_id')
        return query.filter(UserModel.user_id == user_id).first()

    def resolve_computer(self, info, **kwargs):
        query = Computer.get_query(info)
        computer_id = kwargs.get('computer_id')
        return query.filter(ComputerModel.computer_id == computer_id).first()

    def resolve_computerByEDV(self, info, **kwargs):
        query = Computer.get_query(info)
        edv = kwargs.get('edv')
        return query.filter(ComputerModel.edv == edv).first()


    def resolve_os(self, info, **kwargs):
        query = OS.get_query(info)
        os_id = kwargs.get('os_id')
        return query.filter(OSModel.os_id == os_id).first()

    def resolve_mainboard(self, info, **kwargs):
        query = Mainboard.get_query(info)
        mainboard_id = kwargs.get('mainboard_id')
        return query.filter(MainboardModel.mainboard_id == mainboard_id).first()

    def resolve_ram(self, info, **kwargs):
        query = Ram.get_query(info)
        ram_id = kwargs.get('ram_id')
        return query.filter(RamModel.ram_id == ram_id).first()

    def resolve_processor(self, info, **kwargs):
        query = Processor.get_query(info)
        processor_id = kwargs.get('processor_id')
        return query.filter(ProcessorModel.processor_id == processor_id).first()

    def resolve_pcie(self, info, **kwargs):
        query = Pcie.get_query(info)
        pcie_id = kwargs.get('pcie_id')
        return query.filter(PcieModel.pcie_id == pcie_id).first()

    def resolve_software(self, info, **kwargs):
        query = Software.get_query(info)
        software_id = kwargs.get('software_id')
        return query.filter(SoftwareModel.software_id == software_id).first()

    def resolve_mac_adress(self, info, **kwargs):
        query = MacAddress.get_query(info)
        computer_id = kwargs.get('computer_id')
        return query.filter(MacAddressModel.computer_id == computer_id).first()



print("Hello from schema.py")
schema = graphene.Schema(query=Query)
