# Script para gerar hash de senha usando bcrypt
from security import get_password_hash

password = "12345678"
hashed = get_password_hash(password)
print(f"Hash para senha '{password}':")
print(hashed)
print("\nSQL para inserir usuário:")
print(f"INSERT INTO users (email, hashed_password, full_name, role_id, approved) VALUES ('kaio@gmail.com', '{hashed}', 'Kaio', 3, true);")
print(f"INSERT INTO users (email, hashed_password, full_name, role_id, approved) VALUES ('jonas@gmail.com', '{hashed}', 'Jonas', 3, true);")
