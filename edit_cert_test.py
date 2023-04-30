import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import utils.datetime_id as id
import data.data_api as data_api
import os
import traceback
import pandas as pd
from datetime import datetime
import random
import data.data_api as data_api

ROLES = ['Administrador']
NOMBRES = []
NUEVOS_NOMBRES = []
PRECIOS = []
NUMSCONSIG = []
DESCS = []
NIVELES = ['pregrado', 'posgrado']
CAMBIO_GRATUITO = [True, False]

def edit_cert_test(driver, DF, caso, rol, nombre, nuevo_nombre, nivel, precio, recaudo, desc, programas, cambio_gratuito):

    UAC = 5
    passed = 0

    FUNC_STR = 'Editar Certificado'
    PARAMS_STR = f'Nombre: {nombre}\nNuevo Nombre: {nuevo_nombre}\nNivel: {nivel}\nPrecio: {precio}\nNum Consig: {recaudo}\nDesc: {desc}\nProgramas: {programas}\nCambio Gratuito: {cambio_gratuito}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)

        shared.select_module(driver, 'Ver certificados')
        time.sleep(10)

        shared.search(driver, 'Certificados', nombre)

        shared.click_edit_button(driver, 'Certificados', 0)

        time.sleep(5)

        shared.enter_input_value(driver, 'Nombre', nuevo_nombre)
        shared.select_value(driver, 'Nivel', nivel)

        # [UAC] Los programas se filtran de acuerdo al grupo seleccionado
        df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])
        result = shared.UAC_check_two_lists(shared.get_dropdown_multiselect_values(driver, 'Programa'),
                                             df.loc[df['nivel'] == nivel.lower(), 'programa'].tolist())
        passed += shared.evaluate_UAC_result(result)
        shared.press_esc_key(driver)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los programas se filtran de acuerdo al grupo seleccionado', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        shared.enter_input_value(driver, 'Precio', precio)
        shared.enter_input_value(driver, 'Recaudo', recaudo)
        shared.enter_textarea_value(driver, 'Descripción', desc)
        shared.multiselect_values(driver, 'Programas', programas)
        shared.press_esc_key(driver)

        gratuito = shared.get_checkbox_value(driver, 'Certificado Gratuito') 
        if cambio_gratuito:
            shared.click_checkbox(driver, 'Certificado Gratuito')
            gratuito = not gratuito

        time.sleep(5)
        shared.click_button(driver, 'Guardar')
        
        time.sleep(10)

        # [UAC] El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El rol seleccionado se mantiene tras enviar el formulario', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        shared.search(driver, 'Certificados', nombre)

        # [UAC] El sistema evita guardar dos certificados con el mismo nombre
        result = shared.UAC_check_unique_record(driver, 'Certificados', nombre)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El sistema evita guardar dos certificados con el mismo nombre', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK
        
        # [UAC] El certificado se guarda con los datos correctos
        result = shared.UAC_validate_saved_record(driver, 'Certificados', [nuevo_nombre, nivel, 'Habilitado'], 0)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El certificado se guarda con los datos correctos', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
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
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'Los datos del certificado aparecen correctamente en el modo edición', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        print(f'EDIT CERT: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'EDIT CERT: {passed}/{UAC} UAC PASSED')
        return DF


if __name__ == "__main__":

    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 35 # suma de todos los time sleep en la función

    for i in range(nexp):

        rol = random.choice(ROLES)
        nombre = NOMBRES[i]
        nuevo_nombre = NUEVOS_NOMBRES[i]
        precio = random.choice(PRECIOS)
        numconsig = random.choice(NUMSCONSIG)
        desc = random.choice(DESCS)
        nivel = random.choice(NIVELES)
        cambio_gratuito = random.choice(CAMBIO_GRATUITO)

        programs = sorted(df.loc[df['nivel'] == nivel.lower(), 'programa'].tolist())
        num_programs = random.randint(1, 5)
        # Determine the starting index of the consecutive programs
        start_index = random.randint(0, len(programs) - num_programs)
        # Select the consecutive programs
        random_programs = programs[start_index:start_index + num_programs]

        DF = edit_cert_test(driver, DF, caso=i+1, rol=rol, nombre=nombre, nuevo_nombre=nuevo_nombre, nivel=nivel, precio=precio, recaudo=numconsig, desc=desc, programas=random_programs, cambio_gratuito=cambio_gratuito)

        iteration_time = time.time() - start_time - total_time
        total_time += iteration_time

        print(f"Caso {i+1} tomó: {datetime.timedelta(seconds=iteration_time)}")
        print(f"Caso {i+1} sin espera tomó aprox.: {datetime.timedelta(seconds=iteration_time - wait)}")

    avg_time_per_iteration = total_time / nexp
    total_time = time.time() - start_time

    print('\n\n\n')
    print(f"Tiempo promedio por caso: {datetime.timedelta(seconds=avg_time_per_iteration)}")
    print(f"Tiempo promedio aprox. por caso sin espera: {datetime.timedelta(seconds=avg_time_per_iteration - wait)}") 
    print(f"Tiempo total para {nexp} casos: {datetime.timedelta(seconds=total_time)}")
    print(f"Tiempo total aprox. para {nexp} casos sin espera: {datetime.timedelta(seconds=total_time - wait * nexp)}")

    DF.to_excel(r'results\edit_cert_test_results.xlsx', index=False)
