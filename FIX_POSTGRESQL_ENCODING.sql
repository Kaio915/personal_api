-- ==========================================
-- SCRIPT PARA RESOLVER PROBLEMA DE ENCODING
-- ==========================================
-- Execute este script no pgAdmin para mudar
-- a configuração de mensagens do PostgreSQL

-- 1. Muda para mensagens em inglês (evita problemas de encoding)
ALTER DATABASE personaltrainer SET lc_messages TO 'C';

-- 2. Força UTF-8 como encoding padrão
ALTER DATABASE personaltrainer SET client_encoding TO 'UTF8';

-- 3. Suprime avisos (mostra apenas erros)
ALTER DATABASE personaltrainer SET client_min_messages TO 'ERROR';

-- 4. Para aplicar as mudanças, desconecte e reconecte ao banco
-- ou reinicie o serviço do PostgreSQL

-- Verifica as configurações
SELECT name, setting 
FROM pg_settings 
WHERE name IN ('lc_messages', 'client_encoding', 'client_min_messages');
