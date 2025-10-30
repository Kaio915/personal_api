# psycopg2_patch.py
# Patch para fazer psycopg2 ignorar erros de encoding do PostgreSQL

import sys

# Monkey-patch da função _connect do psycopg2
def patch_psycopg2():
    import psycopg2
    original_connect = psycopg2._connect
    
    def patched_connect(dsn, connection_factory=None, cursor_factory=None, **kwargs):
        # Tenta conectar com encoding Latin1 primeiro para evitar erros
        if 'client_encoding' not in dsn and 'client_encoding' not in kwargs:
            # Força Latin1 durante conexão inicial
            if '?' in dsn:
                dsn += '&client_encoding=latin1'
            else:
                dsn += '?client_encoding=latin1'
        
        try:
            conn = original_connect(dsn, connection_factory, cursor_factory, **kwargs)
            # Após conectar, tenta mudar para UTF8
            try:
                with conn.cursor() as cur:
                    cur.execute("SET client_encoding TO 'UTF8'")
                conn.commit()
            except:
                pass  # Se falhar, mantém Latin1
            return conn
        except UnicodeDecodeError:
            # Se ainda falhar, tenta sem nenhum encoding específico
            dsn_clean = dsn.replace('client_encoding=latin1', '').replace('client_encoding=utf8', '')
            return original_connect(dsn_clean, connection_factory, cursor_factory, **kwargs)
    
    psycopg2._connect = patched_connect
    psycopg2.connect = patched_connect

# Aplica o patch
try:
    patch_psycopg2()
    print("✅ Patch do psycopg2 aplicado")
except Exception as e:
    print(f"⚠️ Não foi possível aplicar patch: {e}")
