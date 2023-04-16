import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import os
import traceback
import data.data_api as data_api

def aggr_sol_test(driver, rol, nombres, apellidos, tipo_doc, num_doc, email, celular, grupo, programa, estado_usu, cert, observaciones, medio_pago, num_consig, nota_interna, fecha_grado_retiro=None):

    UAC = 5
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Solicitudes')
        time.sleep(5)
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
        
        # Los programas se filtran de acuerdo al grupo seleccionado
        df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])
        result = shared.UAC_check_two_lists(shared.get_select_dropdown_values(driver, 'Programa'),
                                             df.loc[df['nivel'] == grupo.lower(), 'programa'].tolist())
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)

        shared.select_value(driver, 'Programa', programa)
        shared.select_value(driver, 'Estado', estado_usu)
        time.sleep(1)
        if estado_usu != 'Estudiante Activo':
            shared.set_date_field_value(driver, 2, 'Fecha de grado/retiro', fecha_grado_retiro)
        shared.select_value(driver, 'Certificado', cert)
        shared.enter_textarea_value(driver, 'Observaciones', observaciones)
        shared.select_value(driver, 'Medio de pago', medio_pago)
        shared.press_esc_key(driver)
        shared.enter_input_value(driver, 'Numero de consignación', num_consig) # spelling error
        shared.enter_input_value(driver, 'Soporte de pago', os.path.abspath(r'utils\files\soporte.pdf'), mode=1)
        shared.enter_textarea_value(driver, 'Nota interna', nota_interna)
        shared.click_button(driver, 'Crear')
        time.sleep(2)
      
        try:
            # La solicitud se guarda con los datos correctos
            result = shared.UAC_validate_saved_record(driver, 'Solicitudes', [None, f'{nombres} {apellidos}', None, 'Radicado'], 0) # idx 0 because oredered by update time desc
            passed += shared.evaluate_UAC_result(result)

            passed += 1 # El sistema redirige a la tabla de solicitudes tras enviar el formulario

        except:
            shared.select_module(driver, 'Solicitudes')
            time.sleep(10)
            # La solicitud se guarda con los datos correctos
            result = shared.UAC_validate_saved_record(driver, 'Solicitudes', [None, f'{nombres} {apellidos}', None, 'Radicado'], 0) # idx 0 because oredered by update time desc
            passed += shared.evaluate_UAC_result(result)

            passed += 0 # El sistema redirige a la tabla de solicitudes tras enviar el formulario

        # El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)

        # Los datos del certificado aparecen correctamente en el modo edición
        shared.click_edit_button(driver, 'Solicitudes', 0, 0)   

        time.sleep(2)

        result = shared.UAC_compare_form_fields([shared.get_input_value(driver, 'Nombres'),
                                                shared.get_input_value(driver, 'Apellidos'),
                                                shared.get_input_value(driver, 'Documento'),
                                                shared.get_input_value(driver, 'Tipo de pago'),
                                                shared.get_input_value(driver, 'Numero consignación'),
                                                shared.get_input_value(driver, 'Certificado'),
                                                shared.get_textarea_value(driver, 'Observaciones')
                                                ], [nombres, apellidos, num_doc, medio_pago, num_consig, cert, observaciones])
        passed += shared.evaluate_UAC_result(result)

        print(f'AGGR SOL: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'AGGR SOL: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))
    aggr_sol_test(driver, 
                  rol='Administrador',
                  nombres='Alicia', 
                  apellidos='Smith', 
                  tipo_doc='C.C.', 
                  num_doc=f'{id.get_id_()}', 
                  email='alice@gmail.com', 
                  celular='3100000000', 
                  grupo='Pregrado', 
                  programa='Ingeniería Agrícola', 
                  estado_usu='Egresado', 
                  cert='Plan de estudio extenso pregrado', 
                  observaciones='observaciones', 
                  medio_pago='Banco', 
                  num_consig='2023000', 
                  nota_interna='nota interna',
                  fecha_grado_retiro='2023-03-01')
    