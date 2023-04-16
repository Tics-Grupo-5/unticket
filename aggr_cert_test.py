import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import lib.logout_lib as logout
import utils.datetime_id as id
import traceback
import data.data_api as data_api

def aggr_cert_test(driver, rol, nombre, precio, recaudo, desc, nivel, programas, gratuito):

    UAC = 7
    passed = 0

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Ver certificados')
        time.sleep(2)
        shared.click_button(driver, 'Agregar')
        time.sleep(2)
        shared.enter_input_value(driver, 'Nombre', nombre)
        shared.select_value(driver, 'Nivel', nivel)

        # [UAC] Los programas se filtran de acuerdo al grupo seleccionado
        df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])
        result = shared.UAC_check_two_lists(shared.get_dropdown_multiselect_values(driver, 'Programa'),
                                             df.loc[df['nivel'] == nivel.lower(), 'programa'].tolist())
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)
        # END UAC CHECK

        shared.enter_input_value(driver, 'Precio', precio)
        shared.enter_input_value(driver, 'Recaudo', recaudo)
        shared.enter_textarea_value(driver, 'Descripción', desc)
        shared.multiselect_values(driver, 'Programas', programas)
        shared.press_esc_key(driver)
        if gratuito:
            shared.click_checkbox(driver, 'Certificado Gratuito')
        shared.click_button(driver, 'Guardar')

        time.sleep(2)

        # [UAC] El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] El sistema evita crear dos certificados con el mismo nombre
        shared.search(driver, 'Certificados', nombre)
        result = shared.UAC_check_unique_record(driver, 'Certificados', nombre)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] El certificado se guarda con los datos correctos y está habilitado
        result = shared.UAC_validate_saved_record(driver, 'Certificados', [nombre, nivel, 'Habilitado'], 0)
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] Los datos del certificado aparecen correctamente en el modo edición
        shared.click_edit_button(driver, 'Certificados', 0)   
        result = shared.UAC_compare_form_fields([shared.get_input_value(driver, 'Nombre'),
                                                shared.get_input_value(driver, 'Nivel'),
                                                shared.get_input_value(driver, 'Precio'),
                                                shared.get_input_value(driver, 'Recaudo'),
                                                shared.get_textarea_value(driver, 'Descripción'),
                                                sorted(shared.get_multiselect_values(driver, 'Programas')),
                                                shared.get_checkbox_value(driver, 'Certificado Gratuito') 
                                                ], [nombre, nivel, precio, recaudo, desc, sorted(programas), gratuito])
        passed += shared.evaluate_UAC_result(result)
        shared.click_button(driver, 'Cerrar', 1)
        # END UAC CHECK

        # [UAC] El certificado aparece en el formulario de AGGR SOL
        shared.select_role(driver, 'Administrador')
        time.sleep(5)
        shared.select_module(driver, 'Solicitudes')
        time.sleep(2)
        shared.click_button(driver, 'Agregar')
        time.sleep(5)
        shared.select_value(driver, 'Grupo', nivel.title()) # titlecase in this form
        shared.select_value(driver, 'Programa', programas[0])
        result = shared.UAC_check_element_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        # [UAC] El certificado aparece en el formulario de NUEVO TICKET
        shared.select_role(driver, 'Solicitante')
        time.sleep(5)
        shared.select_module(driver, 'Nuevo ticket')
        time.sleep(2)
        shared.select_value(driver, 'Programa', programas[0]) # PRECONDITION: Program must be assigned to Solicitante
        result = shared.UAC_check_element_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        passed += shared.evaluate_UAC_result(result)
        # END UAC CHECK

        print(f'AGGR CERT: {passed}/{UAC} UAC PASSED')

    except Exception as e:
        traceback.print_exc()
        print(f'AGGR CERT: {passed}/{UAC} UAC PASSED')

if __name__ == "__main__":

    driver = shared.init_driver()

    login(driver, input('Username: '), getpass('Password: '))

    aggr_cert_test(driver, 
                   rol='Administrador', 
                   nombre=f'Mi Certificado {id.get_id()}', 
                   precio=10000, 
                   recaudo='2023000', 
                   desc='UN Certificado', 
                   nivel='pregrado', 
                   programas=['Ingeniería Agrícola', 'Ingeniería Civil'], # PRECONDITION: Program must be assigned to Solicitante
                   gratuito=True)
    