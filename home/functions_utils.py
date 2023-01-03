import base64
import logging
import traceback
import uuid
import ros_api

from cryptography.fernet import Fernet
from django.conf import settings

"""
Encrypt string in parameter 
:param string 
:return encrypted string
"""


def encrypt(pas):
    try:
        pas = str(pas)
        cipher_pass = Fernet(settings.ENCRYPT_KEY)
        encrypt_pass = cipher_pass.encrypt(pas.encode('ascii'))
        encrypt_pass = base64.urlsafe_b64encode(encrypt_pass).decode("ascii")
        return encrypt_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


"""
Decrypt encrypted string 
:param encrypted string
:return decrypt encrypted string
"""


def decrypt(pas):
    try:
        pas = base64.urlsafe_b64decode(pas)
        cipher_pass = Fernet(settings.ENCRYPT_KEY)
        decod_pass = cipher_pass.decrypt(pas).decode("ascii")
        return decod_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


"""
:return unique string
"""


def generate_serial_number():
    return str(uuid.uuid4())


"""
:param ipaddress correspond of ip address of interface 
:param user 
:param password 
"""


class Mikrotik:
    def __init__(self, ipaddress, user, password):
        self.ipaddress = ipaddress
        self.user = user
        self.password = password
        self.router = ros_api.Api(self.ipaddress, user=self.user, password=self.password)

    """
    :return True if interface is online
    """

    def is_online(self):
        return self.router.is_alive()

    """
    execute query on router
    :param command 
    :return result of command
    """

    def execute_query(self, command):
        if self.is_online():
            return self.router.talk(command)
        else:
            return "this interface is non online"

    """
    :return informations about differents interfaces on the router with correspondant address ip
    """

    def list_interface_with_ip_address(self):
        ip_address_list = self.router.talk('/ip/address/print')
        interfaces_list = self.router.talk('/interface/print')
        for ipaddress in ip_address_list:
            for interface in interfaces_list:
                if ipaddress['interface'] == interface['name']:
                    interface['address'] = ipaddress['address']
                else:
                    interface['address'] = ''
        return interfaces_list

    """
    :return name of router
    """

    def get_router_name(self):
        return self.execute_query("/system/identity/print")[0]['name']

    """
    :return list of actives users
    """

    def get_active_user(self):
        return self.execute_query("/user/active/print")

    """
    :return log of router
    """

    def get_log(self):
        return self.execute_query("/log/print")
