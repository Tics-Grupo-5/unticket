import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback

def des_arch_test(driver, rol, id, file, username):

    UAC = 1
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Mis solicitudes')
        time.sleep(10)

        shared.search(driver, 'Mis Solicitudes', id)

        time.sleep(10)

        shared.descargar_soporte(driver, 0)
        time.sleep(5)

        # [UAC] El archivo se descarga correctamente y con el nombre correcto
        file_name_substr = f'{username}_{id}'
        result = shared.UAC_validate_downloaded_filename(file_name_substr, file)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        print(f'DES ARCH: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'DES ARCH: {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    username = input('Username: ')
    login(driver, username, getpass('Password: '))
    # 0 : soporte
    # 1 : certificado
    des_arch_test(driver, rol='Solicitante', id='1508', file=0, username=username)