import constants
import os


def change_ip():
    constants.client_id = None
    constants.uuid = None
    os.system('pppoe-stop')
    os.system('pppoe-start')
    