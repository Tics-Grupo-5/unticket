import time
from getpass import getpass
from login_test import login_test as login
import lib.shared_lib as shared
import lib.logout_lib as logout
import utils.datetime_id as id
import traceback
import data.data_api as data_api
import random
import pandas as pd
import datetime

ROLES = ['Administrador']
NOMBRES = [ 'Certificado']
PRECIOS = [10000, 20000, 50000, 150000, 0]
NUMSCONSIG = ['2023000', '1234567890']
DESCS = ['Lorem ipsum dolor sit.']
NIVELES = ['pregrado', 'posgrado'] 
GRATUITO = [True, False]

def aggr_cert_test(driver, DF, caso, rol, nombre, precio, recaudo, desc, nivel, programas, gratuito):

    UAC = 6
    passed = 0

    FUNC_STR = 'Agregar Certificado'
    PARAMS_STR = f'Nombre: {nombre}\nPrecio: {precio}\nNum Consig: {recaudo}\nDesc: {desc}\nNivel: {nivel}\nProgramas: {programas}\nGratuito: {gratuito}'
    
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
        result = shared.UAC_check_two_lists(shared.get_dropdown_multiselect_values(driver, 'Programas'),
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
        if gratuito:
            shared.click_checkbox(driver, 'Certificado Gratuito')
        shared.click_button(driver, 'Guardar')

        time.sleep(2)

        # [UAC] El rol seleccionado se mantiene tras enviar el formulario
        result = shared.UAC_compare_form_fields([shared.get_role(driver)], [rol])
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El rol seleccionado se mantiene tras enviar el formulario', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] El certificado se guarda con los datos correctos y está habilitado
        shared.search(driver, 'Certificados', nombre)
        time.sleep(5)
        result = shared.UAC_validate_saved_record(driver, 'Certificados', [nombre, nivel, 'Habilitado'], 0)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El certificado se guarda con los datos correctos y está habilitado', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        time.sleep(2)

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

        # [UAC] El certificado aparece en el formulario de AGGR SOL
        shared.select_role(driver, 'Administrador')
        time.sleep(5)
        shared.select_module(driver, 'Solicitudes')
        time.sleep(2)
        shared.click_button(driver, 'Agregar')
        time.sleep(10)
        shared.select_value(driver, 'Grupo', nivel.title()) # titlecase in this form
        shared.select_value(driver, 'Programa', programas[0])
        result = shared.UAC_check_element_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El certificado aparece en el formulario de AGGR SOL', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]} para {programas[0]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] El certificado aparece en el formulario de NUEVO TICKET según el programa seleccionado
        shared.select_role(driver, 'Solicitante')
        time.sleep(5)
        shared.select_module(driver, 'Nuevo ticket')
        time.sleep(4)
        shared.select_value(driver, 'Programa', 'Ingeniería Agrícola') # PRECONDITION: Program must be assigned to Solicitante: se escogió Ingeniería Agrícola arbitrariamente.
        result = shared.UAC_check_element_in_dropdown(nombre, shared.get_select_dropdown_values(driver, 'Certificado'))
        # cannot assign tuple values so I initialize this array
        res = [True if result[0] and 'Ingeniería Agrícola' in programas or not result[0] and 'Ingeniería Agrícola' not in programas else False, result[1]]
        passed += shared.evaluate_UAC_result(res)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'El certificado aparece en el formulario de NUEVO TICKET según el programa seleccionado', 
                                 f"{'SI' if res[0] else 'NO'} : {res[1]} para Ingeniería Agrícola",
                                 'PASSED' if res[0] else 'FAILED')
        # END UAC CHECK

        print(f'AGGR CERT: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'AGGR CERT: {passed}/{UAC} UAC PASSED')
        return DF

if __name__ == "__main__":

    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    df = data_api.read_file(r'data\programas.txt', col_names=['nivel', 'programa'])

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 44

    for i in range(nexp):

        rol = random.choice(ROLES)
        nombre = f'{random.choice(NOMBRES)} - {id.get_id_()}'
        precio = random.choice(PRECIOS)
        numconsig = random.choice(NUMSCONSIG)
        desc = random.choice(DESCS)
        nivel = random.choice(NIVELES)
        gratuito = random.choice(GRATUITO)

        programs = sorted(df.loc[df['nivel'] == nivel.lower(), 'programa'].tolist())
        num_programs = random.randint(1, 5)
        # Determine the starting index of the consecutive programs
        start_index = random.randint(0, len(programs) - num_programs)
        # Select the consecutive programs
        random_programs = programs[start_index:start_index + num_programs]

        DF = aggr_cert_test(driver, DF, caso=i+1, rol=rol, nombre=nombre, precio=precio, recaudo=numconsig, desc=desc, nivel=nivel, programas=random_programs, gratuito=gratuito)

        iteration_time = time.time() - start_time - total_time
        total_time += iteration_time

        print(f"Caso {i+1} tomó: {datetime.timedelta(seconds=iteration_time)}")
        print(f"Caso {i+1} sin espera tomó aprox.: {datetime.timedelta(seconds=iteration_time - wait)}")

    avg_time_per_iteration = total_time / nexp
    total_time = time.time() - start_time

    print('\n\n\n')
    print(f"Tiempo promedio por caso: {datetime.timedelta(seconds=avg_time_per_iteration)}")
    print(f"Tiempo promedio aprox. por caso sin espera: {datetime.timedelta(seconds=avg_time_per_iteration - wait)}") # 42 es el tiempo de todos los time.sleep sin contar funciones en shared
    print(f"Tiempo total para {nexp} casos: {datetime.timedelta(seconds=total_time)}")
    print(f"Tiempo total aprox. para {nexp} casos sin espera: {datetime.timedelta(seconds=total_time - wait * nexp)}")

    DF.to_excel(r'results\aggr_cert_test_results.xlsx', index=False)