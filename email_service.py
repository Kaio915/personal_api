# email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

# Configurações de email (você precisará configurar com suas credenciais)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "seu-email@gmail.com")  # Configure no .env
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "sua-senha-app")  # Configure no .env

def send_verification_code(email: str, code: str, name: str = "Usuário") -> bool:
    """
    Envia código de verificação por email.
    
    Args:
        email: Email do destinatário
        code: Código de verificação de 6 dígitos
        name: Nome do usuário
    
    Returns:
        True se enviado com sucesso, False caso contrário
    """
    try:
        # Criar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = "Código de Verificação - FitConnect"
        message["From"] = f"FitConnect <{SMTP_EMAIL}>"
        message["To"] = email

        # HTML do email
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #1976d2; padding: 20px; text-align: center;">
              <h1 style="color: white; margin: 0;">FitConnect</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f5f5f5;">
              <h2 style="color: #333;">Olá, {name}!</h2>
              
              <p style="color: #666; font-size: 16px;">
                Você solicitou a redefinição de senha. Use o código abaixo para continuar:
              </p>
              
              <div style="background-color: white; padding: 20px; text-align: center; 
                          border-radius: 8px; margin: 20px 0;">
                <div style="font-size: 32px; font-weight: bold; color: #1976d2; 
                            letter-spacing: 8px; font-family: 'Courier New', monospace;">
                  {code}
                </div>
              </div>
              
              <p style="color: #666; font-size: 14px;">
                Este código é válido por <strong>10 minutos</strong>.
              </p>
              
              <p style="color: #999; font-size: 13px; margin-top: 30px;">
                Se você não solicitou esta alteração, ignore este email. 
                Sua senha permanecerá inalterada.
              </p>
            </div>
            
            <div style="background-color: #333; padding: 15px; text-align: center;">
              <p style="color: #999; font-size: 12px; margin: 0;">
                © 2025 FitConnect. Todos os direitos reservados.
              </p>
            </div>
          </body>
        </html>
        """
        
        # Texto alternativo (para clientes que não suportam HTML)
        text = f"""
        Olá, {name}!
        
        Você solicitou a redefinição de senha no FitConnect.
        
        Seu código de verificação é: {code}
        
        Este código é válido por 10 minutos.
        
        Se você não solicitou esta alteração, ignore este email.
        
        ---
        FitConnect
        """
        
        # Adicionar partes ao email
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Enviar email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, email, message.as_string())
        
        print(f"✉️ Email enviado para {email} com código: {code}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False


def send_password_changed_notification(email: str, name: str = "Usuário") -> bool:
    """
    Envia notificação de que a senha foi alterada com sucesso.
    """
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Senha Alterada - FitConnect"
        message["From"] = f"FitConnect <{SMTP_EMAIL}>"
        message["To"] = email

        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #4caf50; padding: 20px; text-align: center;">
              <h1 style="color: white; margin: 0;">FitConnect</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f5f5f5;">
              <h2 style="color: #333;">Senha Alterada com Sucesso!</h2>
              
              <p style="color: #666; font-size: 16px;">
                Olá, {name}!
              </p>
              
              <p style="color: #666; font-size: 16px;">
                Sua senha foi alterada com sucesso. Você já pode fazer login com sua nova senha.
              </p>
              
              <p style="color: #999; font-size: 13px; margin-top: 30px;">
                Se você não realizou esta alteração, entre em contato conosco imediatamente.
              </p>
            </div>
            
            <div style="background-color: #333; padding: 15px; text-align: center;">
              <p style="color: #999; font-size: 12px; margin: 0;">
                © 2025 FitConnect. Todos os direitos reservados.
              </p>
            </div>
          </body>
        </html>
        """

        part = MIMEText(html, "html")
        message.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, email, message.as_string())
        
        print(f"✉️ Notificação de senha alterada enviada para {email}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar notificação: {e}")
        return False
