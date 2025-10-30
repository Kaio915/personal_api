import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        database='personaltrainer',
        user='postgres',
        password='postgres'
    )
    print("✅ Conectou com senha 'postgres'!")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"Total de usuários: {count}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Erro: {e}")
