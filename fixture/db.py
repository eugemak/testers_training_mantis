
import pymysql.cursors
from model.group_m import Group
from model.contact_m import Contact
from model.contact_in_group_m import ContactInGroup


class DbFixture:

    def __init__(self, host=None, database=None, user=None, password=None):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=database, user=user, password=password, autocommit=True)

    def get_group_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                list.append(Group(group_id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return list

    def get_contact_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, firstname, lastname from addressbook")
            for row in cursor:
                (user_id, firstname, lastname) = row
                list.append(Contact(user_id=str(id), firstname=firstname, lastname=lastname))
        finally:
            cursor.close()
        return list

    def get_contact_in_group(self, user_id, group_id):
        list = []
        cursor = self.connection.cursor()
        try:
            sql = ("select id, group_id from address_in_groups where id = '%s' and group_id = '%s'" % (user_id, group_id))
            cursor.execute(sql)
            for row in cursor:
                (id, group_id) = row
                list.append(ContactInGroup(user_id=str(id), group_id=str(group_id)))
        finally:
            cursor.close()
        return list

    def get_all_users_in_all_groups(self):
        list = []
        cursor = self.connection.cursor()
        try:
            sql = "select id, group_id from address_in_groups"
            cursor.execute(sql)
            for row in cursor:
                (id, group_id) = row
                list.append(ContactInGroup(user_id=str(id), group_id=str(group_id)))
        finally:
            cursor.close()
        return list

    def destroy(self):
        self.connection.close()
