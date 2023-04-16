import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback

def dhab_cert_test(driver, rol, nombre):

    UAC = 3
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Ver certificados')
        time.sleep(10)

        shared.search(driver, 'Certificados', nombre)

        old_status = shared.read_cert_status(driver, 0)
        print(old_status)

        shared.click_eye_button(driver, 'Certificados', 0)

        time.sleep(5)

        shared.search(driver, 'Certificados', nombre)

        # [UAC] Al deshabilitar/habilitar el certificado, el estado cambia correctamente
        new_status = 'Habilitado' if old_status == 'Deshabilitado' else 'Deshabilitado'
        result = shared.UAC_validate_saved_record(driver, 'Certificados', [nombre, None, new_status], 0)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # Los datos del certificado aparecen correctamente en el modo edición
        shared.click_edit_button(driver, 'Certificados', 0)   

        time.sleep(5)

        nivel = shared.get_input_value(driver, 'Nivel')
        programas = shared.get_multiselect_values(driver, 'Programas')

        shared.click_button(driver, 'Cerrar', 1)

        # [UAC] Al deshabilitar/habilitar el certificado, no aparece/aparece en el formulario de AGGR SOL
        shared.select_role(driver, 'Administrador')
        time.sleep(5)
        shared.select_module(driver, 'Solicitudes')
        time.sleep(2)
        shared.click_button(driver, 'Agregar')
        time.sleep(10)
        shared.select_value(driver, 'Grupo', nivel.title()) # titlecase in this form
        shared.select_value(driver, 'Programa', programas[0])
        if new_status == 'Habilitado':
            result = shared.UAC_check_element_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        else:
            result = shared.UAC_check_element_not_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] Al deshabilitar/habilitar el certificado, no aparece/aparece en el formulario de NUEVO TICKET
        shared.select_role(driver, 'Solicitante')
        time.sleep(5)
        shared.select_module(driver, 'Nuevo ticket')
        time.sleep(2)
        shared.select_value(driver, 'Programa', programas[0]) # PRECONDITION: Program must be assigned to Solicitante
        if new_status == 'Habilitado':
            result = shared.UAC_check_element_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        else:
            result = shared.UAC_check_element_not_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        print(f'DHAB CERT: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'DHAB CERT: {passed}/{UAC} UAC PASSED')


if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    dhab_cert_test(driver, rol='Administrador', nombre='Mi Certificado 642cdf22')