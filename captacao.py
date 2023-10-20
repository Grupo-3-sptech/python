from mysql.connector import connect
import psutil
import platform
import time
import mysql.connector
from datetime import datetime

def mysql_connection(host, user, passwd, database=None):
    connection = connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )
    return connection

connection = mysql_connection('localhost', 'root', '5505', 'MedConnect')

while True:
    memoriaPorcentagem = psutil.virtual_memory()[2]
    cpuPorcentagem = psutil.cpu_percent(None)
    discoPorcentagem = psutil.disk_usage('/')[3]
    interval = 1
    statusRede = 0
    network_connections = psutil.net_connections()

    network_active = any(conn.status == psutil.CONN_ESTABLISHED for conn in network_connections)

    

    print ("\nINFORMAÇÕES SOBRE A REDE: ")

    if network_active:

        print ("A rede está ativa.")
        statusRede= 1
    else:

        print ("A rede não está ativa.")




    cursor = connection.cursor()


    horarioAtual = datetime.now()
    horarioFormatado = horarioAtual.strftime('%Y-%m-%d %H:%M:%S')
    
    ins = [cpuPorcentagem, memoriaPorcentagem, discoPorcentagem, statusRede]
    componentes = [1,2,3,4]
    cursor = connection.cursor()
    
    for i in range(len(ins)):
        
        dado = ins[i]
        
        componente = componentes[i]

    
        query = "INSERT INTO Registros (dado, fkRoboRegistro, fkComponente, HorarioDado) VALUES (%s, 1, %s, %s)"

    
        cursor.execute(query, (dado, componente,horarioFormatado))


        connection.commit()
    print("\nINFORMAÇÕES SOBRE PROCESSAMENTO: ")
    print('Porcentagem utilizada do Processador: ',cpuPorcentagem,'\nPorcentagem utilizada de memoria: ', memoriaPorcentagem,'\nPorcentagem do disco sendo utilizada:', discoPorcentagem,'\nStatus da rede: ',statusRede)
   
    
       


    time.sleep(2)

cursor.close()
connection.close()
    
