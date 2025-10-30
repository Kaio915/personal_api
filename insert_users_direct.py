import psycopg2
from psycopg2.extensions import connection, ISOLATION_LEVEL_AUTOCOMMIT

# Conecta diretamente ao PostgreSQL sem SQLAlchemy
conn_params = {
    'host': 'localhost',
    'database': 'personaltrainer',
    'user': 'postgres',
    'password': '123456',
    'client_encoding': 'utf8',
    'options': '-c client_min_messages=ERROR'  # Suprime WARNINGS e NOTICES
}

try:
    # Tenta conectar com configurações especiais
    conn = psycopg2.connect(**conn_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    print("✅ Conectado ao PostgreSQL com sucesso!\n")
    
    # Lê e executa o SQL
    with open('insert_test_users.sql', 'r', encoding='utf-8') as f:
        sql_commands = f.read()
    
    # Divide em comandos individuais e executa
    for command in sql_commands.split(';'):
        command = command.strip()
        if command and not command.startswith('--'):
            try:
                cursor.execute(command)
                if cursor.description:  # Se tem resultados
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
            except Exception as e:
                print(f"Erro ao executar comando: {e}")
                print(f"Comando: {command[:100]}...")
    
    cursor.close()
    conn.close()
    print("\n✅ SQL executado com sucesso!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    print(f"Tipo do erro: {type(e)}")
