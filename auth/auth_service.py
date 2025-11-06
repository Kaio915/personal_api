# auth/auth_service.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import JWTError, jwt

from database import get_db
import os
from users import user_repository
from security import verify_password, SECRET_KEY, ALGORITHM, TokenData
from users.user_models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def authenticate_user(db: Session, email: str, password: str, user_type: str = None):
    """
    Autentica usuário com validação de role
    user_type: 'student' ou 'trainer' (opcional, usado para validação)
    """
    user = user_repository.get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    # Validação de role: apenas admin pode logar em qualquer tipo
    if user_type and user.role.name != "admin":
        if user_type == "student" and user.role.name != "aluno":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este usuário não é um aluno. Tente fazer login como Personal Trainer."
            )
        elif user_type == "trainer" and user.role.name != "personal":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este usuário não é um Personal Trainer. Tente fazer login como Aluno."
            )
    
    # Verifica se o usuário está aprovado (exceto admin)
    if user.role.name != "admin" and not user.approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sua conta ainda não foi aprovada pelo administrador. Aguarde a aprovação."
        )
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = user_repository.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role_name: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if not current_user.role or current_user.role.name != required_role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this user role"
            )
        return current_user
    return role_checker

def reset_password(db: Session, email: str, new_password: str) -> bool:
    """
    Reseta a senha de um usuário pelo email.
    Retorna True se bem-sucedido, False se o email não for encontrado.
    """
    from security import get_password_hash
    
    user = user_repository.get_user_by_email(db, email=email)
    if not user:
        return False
    
    # Atualizar senha
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return True

def request_password_reset_code(db: Session, email: str) -> dict:
    """
    Gera e envia código de verificação para reset de senha.
    """
    from verification_code_model import VerificationCode
    from datetime import datetime, timedelta
    # from email_service import send_verification_code  # Descomentar quando configurar email
    
    # Verificar se usuário existe
    user = user_repository.get_user_by_email(db, email=email)
    if not user:
        return {"success": False, "message": "Email não encontrado"}
    
    # Gerar código
    code = VerificationCode.generate_code()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    # Salvar no banco
    verification = VerificationCode(
        email=email,
        code=code,
        purpose="password_reset",
        expires_at=expires_at
    )
    db.add(verification)
    db.commit()
    
    # Enviar email (será executado apenas se EMAIL_ENABLED=true nas variáveis de ambiente)
    if os.getenv("EMAIL_ENABLED", "false").lower() == "true":
        try:
            from email_service import send_verification_code
            send_verification_code(email, code, user.full_name or "Usuário")
        except Exception as e:
            # Não falhar o fluxo por causa do email — apenas logar o erro
            print(f"❌ Falha ao enviar email de código para {email}: {e}")
    
    # Em desenvolvimento, retornar o código (REMOVER EM PRODUÇÃO!)
    print(f"🔑 Código de verificação para {email}: {code}")
    
    return {
        "success": True, 
        "message": "Código enviado",
        "code": code  # REMOVER EM PRODUÇÃO!
    }

def verify_code_and_reset_password(db: Session, email: str, code: str, new_password: str) -> dict:
    """
    Verifica o código e reseta a senha.
    """
    from verification_code_model import VerificationCode
    from security import get_password_hash
    from datetime import datetime
    # from email_service import send_password_changed_notification  # Descomentar quando configurar
    
    # Buscar código válido mais recente
    verification = db.query(VerificationCode).filter(
        VerificationCode.email == email,
        VerificationCode.code == code,
        VerificationCode.purpose == "password_reset",
        VerificationCode.used == 0
    ).order_by(VerificationCode.created_at.desc()).first()
    
    if not verification:
        return {"success": False, "message": "Código inválido"}
    
    if not verification.is_valid():
        return {"success": False, "message": "Código expirado ou já utilizado"}
    
    # Buscar usuário
    user = user_repository.get_user_by_email(db, email=email)
    if not user:
        return {"success": False, "message": "Usuário não encontrado"}
    
    # Marcar código como usado
    verification.mark_as_used()
    
    # Atualizar senha
    user.hashed_password = get_password_hash(new_password)
    
    db.commit()
    db.refresh(user)
    
    # Enviar notificação (será executado apenas se EMAIL_ENABLED=true nas variáveis de ambiente)
    if os.getenv("EMAIL_ENABLED", "false").lower() == "true":
        try:
            from email_service import send_password_changed_notification
            send_password_changed_notification(email, user.full_name or "Usuário")
        except Exception as e:
            print(f"❌ Falha ao enviar notificação de senha alterada para {email}: {e}")
    
    return {"success": True, "message": "Senha alterada com sucesso"}