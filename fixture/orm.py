from pony.orm import *
from datetime import datetime
from pony.converting import str2datetime
from model.group_m import Group
from model.contact_m import Contact
from pymysql.converters import decoders


class ORMFixture:

    db = Database()

    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        contacts = Set(lambda: ORMFixture.ORMContact, table="address_in_groups", column="id", reverse="groups", lazy=True)

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        groups = Set(lambda: ORMFixture.ORMGroup, table="address_in_groups", column="group_id", reverse="contacts", lazy=True)
        deprecated = Optional(str, column='deprecated')
        address = Optional(str, column='address')
        home_phone = Optional(str, column='home')
        work_phone = Optional(str, column='work')
        mobile_phone = Optional(str, column='mobile')
        secondary_phone = Optional(str, column='phone2')
        email = Optional(str, column='email')
        email2 = Optional(str, column='email2')
        email3 = Optional(str, column='email3')

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password, conv=decoders)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_groups_to_model(self, groups):
        def convert(group):
            return Group(group_id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))

    @db_session
    def get_group_list(self):
        return self.convert_groups_to_model(select(g for g in ORMFixture.ORMGroup))

    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(user_id=str(contact.id), firstname=contact.firstname, lastname=contact.lastname)
        return list(map(convert, contacts))

    @db_session
    def get_contact_list(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))

    def convert_contacts_to_model_extended(self, contacts):
        def convert(contact):
            return Contact(user_id=str(contact.id), firstname=contact.firstname, lastname=contact.lastname,
                           home_phone=contact.home_phone, work_phone=contact.work_phone,
                           mobile_phone=contact.mobile_phone, secondary_phone=contact.secondary_phone,
                           email=contact.email, email2=contact.email2, email3=contact.email3)
        return list(map(convert, contacts))

    @db_session
    def get_contact_list_extended(self):
        return self.convert_contacts_to_model_extended(select(c for c in ORMFixture.ORMContact if c.deprecated is None))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.group_id))[0]
        return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.group_id))
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if orm_group not in c.groups))

