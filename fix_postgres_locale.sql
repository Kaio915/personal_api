-- Define mensagens do PostgreSQL em inglês para evitar problemas de encoding
-- No Windows, o locale para inglês é diferente
ALTER DATABASE personaltrainer SET lc_messages TO 'English_United States.1252';

-- Também define client_encoding para UTF8
ALTER DATABASE personaltrainer SET client_encoding TO 'UTF8';
