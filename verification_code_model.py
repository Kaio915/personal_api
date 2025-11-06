# verification_code_model.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta
from database import Base
import random

class VerificationCode(Base):
    __tablename__ = "verification_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    code = Column(String(6), nullable=False)
    purpose = Column(String, nullable=False)  # 'password_reset', 'email_verification', etc
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Integer, default=0)  # 0 = não usado, 1 = usado
    
    @staticmethod
    def generate_code() -> str:
        """Gera um código de 6 dígitos"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    def is_valid(self) -> bool:
        """Verifica se o código ainda é válido"""
        return not self.used and datetime.utcnow() < self.expires_at
    
    def mark_as_used(self):
        """Marca o código como usado"""
        self.used = 1
