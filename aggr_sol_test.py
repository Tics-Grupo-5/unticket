import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback

def aggr_sol_test(driver, nombres, apellidos, tipo_doc, num_doc, email, celular, grupo, programa, estado_usu, cert, observaciones, medio_pago, num_consig, nota_interna):

    UAC = 1
    passed = 0

    try:

        shared.select_module(driver, 'Solicitudes')
        time.sleep(2)
        shared.click_button(driver, 'Agregar')
        time.sleep(5)
        shared.enter_input_value(driver, 'Nombres', nombres)
        shared.enter_input_value(driver, 'Apellidos', apellidos)
        shared.select_value(driver, 'Tipo de documento', tipo_doc)
        shared.enter_input_value(driver, 'Número de documento', num_doc)
        shared.enter_input_value(driver, 'Correo', email)
        shared.enter_input_value(driver, 'Celular', celular)
        shared.click_checkbox(driver, 'Acepto las políticas')
        shared.select_value(driver, 'Grupo', grupo)
        shared.select_value(driver, 'Programa', programa)
        shared.select_value(driver, 'Estado', estado_usu)
        shared.select_value(driver, 'Certificado', cert)
        shared.enter_textarea_value(driver, 'Observaciones', observaciones)
        time.sleep(2)
        shared.select_value(driver, 'Medio de pago', medio_pago)
        shared.press_esc_key(driver)
        shared.enter_input_value(driver, 'Numero de consignación', num_consig) # spelling error
        shared.enter_input_value(driver, 'Soporte de pago', os.path.abspath(r'utils\files\soporte.pdf'), mode=1)
        shared.enter_textarea_value(driver, 'Nota interna', nota_interna)
        time.sleep(5)
        shared.click_button(driver, 'Crear')
        time.sleep(5)
        # we check first row to see if record was saved : it should work because data is ordered by date descending by default
        result = shared.UAC_validate_saved_record(driver, 'Solicitudes', [None, f'{nombres} {apellidos}', None, 'Radicado'], 0)
        passed += shared.evaluate_UAC_result(result)

        print(f'AGGR SOL: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'AGGR SOL: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    shared.select_role(driver, 'Administrador')
    time.sleep(5)
    aggr_sol_test(driver, nombres='Alicia', apellidos='Smith', tipo_doc='C.C.', num_doc=f'{id.get_id_()}', 
                  email='alice@gmail.com', celular='3100000000', grupo='Pregrado', programa='Ingeniería Agrícola', 
                  estado_usu='Estudiante activo', cert='Plan de estudio extenso pregrado', observaciones='observaciones', 
                  medio_pago='Banco', num_consig='2023000', nota_interna='nota interna')
    