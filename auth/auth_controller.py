# auth/auth_controller.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from . import auth_service
from security import create_access_token, get_current_user
from users.user_models import UserPublic, User

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

class RequestCodeRequest(BaseModel):
    email: str

class VerifyCodeRequest(BaseModel):
    email: str
    code: str
    new_password: str

@router.post("/login")
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_type: str = Query(None, description="Tipo de usuário: 'student' ou 'trainer'")
):
    """
    Login com validação de role:
    - user_type='student': apenas alunos e admin podem logar
    - user_type='trainer': apenas personal trainers e admin podem logar
    - user_type=None: qualquer usuário pode logar (usado para admin)
    """
    user = auth_service.authenticate_user(
        db, 
        email=form_data.username, 
        password=form_data.password,
        user_type=user_type
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": user.email, "role": user.role.name}
    access_token = create_access_token(data=token_data)
    
    # Retornar token + dados do usuário
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "approved": user.approved,
            "role": {
                "id": user.role.id,
                "name": user.role.name
            }
        }
    }

@router.get("/me", response_model=UserPublic)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Retorna os dados do usuário autenticado"""
    return current_user

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset de senha sem token (simplificado para MVP).
    Em produção, deveria enviar email com token de confirmação.
    DEPRECATED: Use /request-reset-code e /verify-reset-code para maior segurança
    """
    success = auth_service.reset_password(db, request.email, request.new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email não encontrado"
        )
    return {"message": "Senha alterada com sucesso"}

@router.post("/request-reset-code")
def request_reset_code(
    request: RequestCodeRequest,
    db: Session = Depends(get_db)
):
    """
    Solicita código de verificação para reset de senha.
    O código será enviado por email (ou console em dev).
    """
    result = auth_service.request_password_reset_code(db, request.email)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["message"]
        )
    
    return {
        "message": "Código de verificação enviado para o email",
        "dev_code": result.get("code")  # Remover em produção!
    }

@router.post("/verify-reset-code")
def verify_reset_code(
    request: VerifyCodeRequest,
    db: Session = Depends(get_db)
):
    """
    Verifica código e redefine a senha.
    """
    result = auth_service.verify_code_and_reset_password(
        db, 
        request.email, 
        request.code, 
        request.new_password
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {"message": "Senha alterada com sucesso"}