import psycopg2

# Conectar ao banco de dados
conn = psycopg2.connect(
    host="localhost",
    database="personaltrainer",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# Verificar todas as conexões
cur.execute("SELECT * FROM connections ORDER BY id DESC LIMIT 10")
connections = cur.fetchall()

print("\n=== ÚLTIMAS 10 CONEXÕES NO BANCO ===")
if connections:
    for conn_data in connections:
        print(f"ID: {conn_data[0]}, Student: {conn_data[1]}, Trainer: {conn_data[2]}, Status: {conn_data[3]}")
else:
    print("Nenhuma conexão encontrada no banco de dados")

# Verificar quantos usuários existem
cur.execute("SELECT id, full_name, role_id FROM users")
users = cur.fetchall()
print("\n=== USUÁRIOS NO BANCO ===")
for user in users:
    role_name = "admin" if user[2] == 1 else "personal" if user[2] == 2 else "aluno"
    print(f"ID: {user[0]}, Nome: {user[1]}, Role: {role_name} ({user[2]})")

cur.close()
conn.close()
