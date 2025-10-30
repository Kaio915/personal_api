import pg8000

# Tenta conectar com pg8000 diretamente
try:
    conn = pg8000.connect(
        host='localhost',
        database='personaltrainer',
        user='postgres',
        password='123456'
    )
    
    print("✅ Conectado com pg8000!")
    
    cursor = conn.cursor()
    
    # Insere usuários
    cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, role_id, approved) 
        VALUES ('kaio@gmail.com', '$2b$12$vTE60.99ojIjrMHqE0PNk.Id2zHEPHpaG26tK5P0MWJyam8P8tX0m', 'Kaio', 3, true)
        ON CONFLICT (email) DO NOTHING
    """)
    
    cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, role_id, approved) 
        VALUES ('jonas@gmail.com', '$2b$12$vTE60.99ojIjrMHqE0PNk.Id2zHEPHpaG26tK5P0MWJyam8P8tX0m', 'Jonas', 3, true)
        ON CONFLICT (email) DO NOTHING
    """)
    
    conn.commit()
    
    # Lista usuários
    cursor.execute("SELECT id, email, full_name, role_id, approved FROM users")
    users = cursor.fetchall()
    print(f"\n📋 Total de usuários: {len(users)}")
    for user in users:
        print(f"  ID: {user[0]}, Email: {user[1]}, Nome: {user[2]}, Role: {user[3]}, Aprovado: {user[4]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Concluído!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
