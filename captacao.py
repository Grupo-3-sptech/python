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

def bytes_para_gb(bytes_value):
    return bytes_value / (1024 ** 3)

def milissegundos_para_segundos(ms_value):
    return ms_value / 1000

connection = mysql_connection('localhost', 'admin', 'admin', 'MedConnect')

while True:

    #CPU
    cpuPorcentagem = psutil.cpu_percent(None)
    frequenciaCpuMhz = psutil.cpu_freq(percpu=False)
    cpuVelocidadeEmGhz = "{:.2f}".format(frequenciaCpuMhz.current / 1000)
    tempoSistema = psutil.cpu_times()[1] 
    processos = len(psutil.pids())

    
    #Memoria
    memoriaPorcentagem = psutil.virtual_memory()[2]
    memoriaTotal = "{:.2f}".format(bytes_para_gb(psutil.virtual_memory().total))
    memoriaUsada = "{:.2f}".format(bytes_para_gb(psutil.virtual_memory().used))
    memoriaSwapPorcentagem = psutil.swap_memory()

    #Disco
    discoPorcentagem = psutil.disk_usage('/')[3]
    discoTempoLeitura = milissegundos_para_segundos(psutil.disk_io_counters(perdisk=False, nowrap=True)[4])
    discoTempoEscrita = milissegundos_para_segundos(psutil.disk_io_counters(perdisk=False, nowrap=True)[5])
    

    #Rede
    interval = 1
    statusRede = 0
    network_connections = psutil.net_connections()
    network_active = any(conn.status == psutil.CONN_ESTABLISHED for conn in network_connections)
    bytes_enviados = psutil.net_io_counters()[0]
    bytes_recebidos = psutil.net_io_counters()[1]

    #Outros
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    print(boot_time)

    

    print ("\nINFORMAÇÕES SOBRE A REDE: ")

    if network_active:

        print ("A rede está ativa.")
        statusRede= 1
    else:

        print ("A rede não está ativa.")




    cursor = connection.cursor()


    horarioAtual = datetime.now()
    horarioFormatado = horarioAtual.strftime('%Y-%m-%d %H:%M:%S')
    
    ins = [cpuPorcentagem, cpuVelocidadeEmGhz, tempoSistema, processos, memoriaPorcentagem, memoriaTotal, memoriaUsada, memoriaSwapPorcentagem, discoPorcentagem, statusRede, discoTempoLeitura, discoTempoEscrita, bytes_enviados, bytes_recebidos]
    componentes = [1,2,3,4,5,6,7,8,9,10, 11, 12, 13, 14]
    
    cursor = connection.cursor()
    """
    for i in range(len(ins)):
        
        dado = ins[i]
        
        componente = componentes[i]

    
        query = "INSERT INTO Registros (dado, fkRoboRegistro, fkComponente, HorarioDado) VALUES (%s, 1, %s, %s)"

    
        cursor.execute(query, (dado, componente,horarioFormatado))


        connection.commit()
       """ 
    print("\nINFORMAÇÕES SOBRE PROCESSAMENTO: ")
    print('Porcentagem utilizada da CPU: ',cpuPorcentagem,
          '\nVelocidade da CPU: ',cpuVelocidadeEmGhz,
          '\nPorcentagem utilizada de memoria: ', memoriaPorcentagem,
          '\nPorcentagem do disco sendo utilizada:', discoPorcentagem,
          '\nTempo de leitura do disco em segundos:', discoTempoLeitura,
          '\nTempo de escrita do disco em segundos:', discoTempoEscrita,
          '\nRede - Bytes enviados:', bytes_enviados,
          '\nRede - Bytes recebidos: ', bytes_recebidos)
   
    
       


    time.sleep(2)

cursor.close()
connection.close()
    
