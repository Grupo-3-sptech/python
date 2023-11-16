import pymssql

ip = '52.7.105.138'
username = 'sa'
database = 'medconnect'
passw = 'medconnect123'


conn = pymssql.connect(server=ip, database=database, user=username, password=passw)

cursor = conn.cursor()

sql_query = """
INSERT INTO Usuario (nome, email, CPF, telefone, senha, fkHospital, fkEscalonamento)
VALUES ('Nome do Novo Usuário', 'email@exemplo.com', '12345678901', '987654321', 'senha123', 1, 1)
"""
cursor.execute(sql_query)
conn.commit()

conn.close()
