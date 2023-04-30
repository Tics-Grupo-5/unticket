import time
import lib.aggr_acl_lib as aggr_acl
from login_test import login_test as login
from getpass import getpass
import lib.shared_lib as shared
import utils.filters as filters
import traceback
import data.data_api as data_api
import random
import pandas as pd
import datetime

ROLES = ['Solicitante']
IDS = []
RESPUESTAS = []

def aggr_acl_test(driver, DF, caso, rol, id, respuesta):

    UAC = 2
    passed = 0

    FUNC_STR = 'Agregar Certificado'
    PARAMS_STR = f'Id: {id}\nRespuesta: {respuesta}'

    try:

        shared.select_role(driver, rol)
        time.sleep(5)
        
        # Add clarification
        shared.select_module(driver, 'Mis solicitudes')
        time.sleep(5)
        
        shared.search(driver, 'Mis Solicitudes', id)
        time.sleep(5)
        
        aggr_acl.click_solicitud(driver, 0)
        time.sleep(5)

        shared.enter_textarea_value(driver, 'Respuesta', respuesta)

        shared.click_button(driver, 'Guardar')
        time.sleep(5)
      
        # [UAC] La solicitud se guarda con los datos correctos y el estado es En trámite
        shared.search(driver, 'Mis Solicitudes', id)
        result = shared.UAC_validate_saved_record(driver, 'Mis Solicitudes', [id, 'En trámite'], 0)
        passed += shared.evaluate_UAC_result(result)
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'La solicitud se guarda con los datos correctos y el estado es En trámite', 
                                 f"{'SI' if result[0] else 'NO'} : {result[1]}",
                                 'PASSED' if result[0] else 'FAILED')
        # END UAC CHECK

        # [UAC] La solicitud es visible con los datos correctos para los diferentes roles
        results = []
        for _rol_ in ['Administrador', 'Gestor 1', 'Gestor 2', 'Recepción']:
            shared.select_role(driver, _rol_)
            time.sleep(5)
            shared.select_module(driver, 'Solicitudes')
            time.sleep(10)
            shared.search(driver, 'Solicitudes', id)
            results.append(shared.UAC_validate_saved_record(driver, 'Solicitudes', [id, None, None, None, 'En trámite'], 0))
        composite_result = shared.evaluate_composite_UAC_result(results)
        passed += composite_result
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR,
                                 'La solicitud es visible con los datos correctos para los diferentes roles', 
                                 f"{'SI' if composite_result == 1 else 'NO'} : {results}",
                                 'PASSED' if composite_result == 1 else 'FAILED')
        # END UAC CHECK

        print(f'AGGR ACL: {passed}/{UAC} UAC PASSED')

        return DF

    except Exception as e:
        traceback.print_exc()
        DF = data_api.write_row_to_df(DF, caso, FUNC_STR, rol, PARAMS_STR, 'EXCEPTION', e, 'EXCEPTION')
        print(f'AGGR ACL: {passed}/{UAC} UAC PASSED')
        return DF

if __name__ == '__main__':
    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    DF = pd.DataFrame(columns=['CASO', 'FUNCIONALIDAD', 'ROL', 'PARAMS', 'UAC', 'SALIDA', 'RESULTADO'])

    driver = shared.init_driver()
    login(driver, input('Username: '), getpass('Password: '))

    start_time = time.time()
    total_time = 0

    nexp = 10
    wait = 85 # suma de todos los time sleep en la función

    for i in range(nexp):

        rol = random.choice(ROLES)
        id = IDS[i]
        respuesta = RESPUESTAS[i]

        DF = aggr_acl_test(driver, DF, caso=i+1, rol=rol, id=id, respuesta=respuesta)

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

    DF.to_excel(r'results\aggr_acl_test_results.xlsx', index=False)

    '''
    aggr_acl_test(driver, rol='Solicitante', id='1508', respuesta='aclaración 1508') # PRECONDICIÓN: Necesita estar en estado Aclaración
    '''


