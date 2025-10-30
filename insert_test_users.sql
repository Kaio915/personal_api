-- Insere usuários de teste com senha '12345678'
-- Hash gerado via bcrypt
INSERT INTO users (email, hashed_password, full_name, role_id, approved) 
VALUES ('kaio@gmail.com', '$2b$12$vTE60.99ojIjrMHqE0PNk.Id2zHEPHpaG26tK5P0MWJyam8P8tX0m', 'Kaio', 3, true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (email, hashed_password, full_name, role_id, approved) 
VALUES ('jonas@gmail.com', '$2b$12$vTE60.99ojIjrMHqE0PNk.Id2zHEPHpaG26tK5P0MWJyam8P8tX0m', 'Jonas', 3, true)
ON CONFLICT (email) DO NOTHING;

-- Verifica quantos usuários foram criados
SELECT COUNT(*) as total_users FROM users;
SELECT id, email, full_name, role_id, approved FROM users;
