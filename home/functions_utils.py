import base64
import logging
import traceback
import uuid
import ros_api
import subprocess
import platform

from cryptography.fernet import Fernet
from django.conf import settings


def encrypt(pas):
    """
    Encrypt string in parameter
    :param string
    :return encrypted string
    """
    try:
        pas = str(pas)
        cipher_pass = Fernet(settings.ENCRYPT_KEY)
        encrypt_pass = cipher_pass.encrypt(pas.encode('ascii'))
        encrypt_pass = base64.urlsafe_b64encode(encrypt_pass).decode("ascii")
        return encrypt_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(pas):
    """
    Decrypt encrypted string
    :param encrypted string
    :return decrypt encrypted string
    """
    try:
        pas = base64.urlsafe_b64decode(pas)
        cipher_pass = Fernet(settings.ENCRYPT_KEY)
        decod_pass = cipher_pass.decrypt(pas).decode("ascii")
        return decod_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def generate_serial_number():
    """
    :return unique string
    """
    return str(uuid.uuid4())


def check_if_router_is_online(ipaddress):
    """
    :return: True if router is online
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ipaddress]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    return not bool(result.returncode)


class Mikrotik:
    """
    :param: ipaddress correspond of ip address of interface
    :param: user of router
    :param: password
    """

    def __init__(self, ipaddress, user, password):
        self.ipaddress = ipaddress
        self.user = user
        self.password = password
        self.router = ros_api.Api(self.ipaddress, user=self.user, password=self.password)

    def is_online(self):
        """
        :return: True if interface is online
        """
        return self.router.is_alive()

    def get_interfaces(self):
        """
        :return: list of interfaces
        """
        result = [{k.replace("-", "_"): v for k, v in information.items()}
                  for information in self.execute_query("/interface/print")]
        return result

    def execute_query(self, command):
        """
        execute query on router
        :param command
        :return: result of command
        """
        if self.is_online():
            return self.router.talk(command)
        else:
            return "this interface is non online"

    def get_router_name(self):
        """
        :return: name of router
        """
        return self.execute_query("/system/identity/print")[0]['name']

    def get_active_users(self):
        """

        :return:list of active users
        """
        result = [{k.replace("-", "_"): v for k, v in information.items()}
                  for information in self.execute_query("/user/active/print")]
        return result

    def get_logs(self):
        """
        :return: logs of router
        """
        result = [{k.replace("-", "_"): v for k, v in information.items()}
                  for information in self.execute_query("/log/print")]
        return result

    def get_available_port(self):
        """

        :return: list of available ports
        """
        result = [{k.replace("-", "_"): v for k, v in information.items()}
                  for information in self.execute_query("/port/print")]
        return result

    def get_router_operating_statistic(self):
        """
        :return: router operating statistic
        """
        result = [{k.replace("-", "_"): v for k, v in information.items()}
                  for information in self.execute_query("/system/resource/print")]
        return result

    def get_ip_address(self):
        """

        :return: interfaces with their ip address
        """
        result = [{k.replace("-", "_"): v for k, v in information.items()}
                  for information in self.execute_query("/ip/address/print")]
        return result

    def get_serial_number(self):
        """
        :return: serial number of router
        """
        result = [{k.replace("-", "_"): v for k, v in information.items()}
                  for information in self.execute_query("/system/routerboard/print")]
        return result

    def check_if_router_is_online(self):
        """
        :return: True if router is online
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', self.ipaddress]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        return not bool(result.returncode)