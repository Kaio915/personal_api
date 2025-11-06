# CONFIGURAÇÃO DE EMAIL SEGURO - FitConnect

## ✅ O que foi implementado:

### Backend:
1. **Tabela `verification_codes`** - Armazena códigos temporários
2. **Modelo `VerificationCode`** - Gerencia códigos de 6 dígitos com expiração de 10 minutos
3. **Serviço de Email** (`email_service.py`) - Envia códigos e notificações
4. **Novos Endpoints**:
   - `POST /auth/request-reset-code` - Solicita código de verificação
   - `POST /auth/verify-reset-code` - Valida código e altera senha
   - `POST /auth/reset-password` - Método antigo (mantido por compatibilidade)

### Segurança Implementada:
- ✅ Código de 6 dígitos aleatório
- ✅ Expiração em 10 minutos
- ✅ Código de uso único (marcado como usado após validação)
- ✅ Emails HTML profissionais
- ✅ Notificação após mudança de senha

---

## 📧 Como Configurar o Email (Produção):

### Opção 1: Gmail (Recomendado para teste)

1. **Habilitar autenticação de 2 fatores** na sua conta Google
2. **Gerar senha de app**:
   - Acesse: https://myaccount.google.com/apppasswords
   - Selecione "App" > "Outro (nome personalizado)" > "FitConnect"
   - Copie a senha gerada (16 caracteres)

3. **Criar arquivo `.env`** na raiz da API:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-app-16-caracteres
```

4. **Descomentar** no `auth_service.py`:
```python
from email_service import send_verification_code
send_verification_code(email, code, user.full_name or "Usuário")
```

### Opção 2: SendGrid (Recomendado para produção)

1. Criar conta em https://sendgrid.com (gratuito até 100 emails/dia)
2. Gerar API Key
3. Modificar `email_service.py` para usar SendGrid API
4. Configurar domínio personalizado (opcional)

### Opção 3: AWS SES (Amazon Simple Email Service)

1. Melhor para alta escala
2. Muito barato (first 62k emails free/month)
3. Requer configuração de domínio verificado

---

## 🚀 Como Usar (Modo Desenvolvimento):

**Atualmente funciona sem configurar email!**

O sistema imprime o código no console do backend:
```
🔑 Código de verificação para user@email.com: 123456
```

E retorna o código na resposta da API (REMOVER EM PRODUÇÃO!):
```json
{
  "message": "Código de verificação enviado para o email",
  "dev_code": "123456"
}
```

---

## 🔒 Medidas de Segurança Adicionais Possíveis:

### 1. **Rate Limiting** (Limitar tentativas):
```python
# Limitar a 3 tentativas de código por hora
# Limitar a 5 solicitações de código por dia
```

### 2. **Captcha** (Prevenir bots):
- Google reCAPTCHA v3
- hCaptcha

### 3. **Perguntas de Segurança**:
- Data de nascimento
- CPF (últimos dígitos)
- Telefone

### 4. **SMS** (Além de email):
- Twilio
- AWS SNS
- Mais caro mas mais seguro

### 5. **Autenticação de 2 Fatores (2FA)**:
- TOTP (Google Authenticator)
- Backup codes

### 6. **Histórico de Logins**:
- Registrar IP, data/hora, dispositivo
- Alertar sobre login suspeito

### 7. **Senha Forte**:
- Mínimo 8 caracteres
- Letra maiúscula, minúscula, número, símbolo
- Verificar contra lista de senhas comuns

---

## 📱 Fluxo do Usuário:

1. **Usuário**: Clica em "Esqueceu a senha?"
2. **Usuário**: Informa email
3. **Sistema**: Gera código de 6 dígitos
4. **Sistema**: Envia código por email (ou mostra no console em dev)
5. **Usuário**: Insere código + nova senha
6. **Sistema**: Valida código (expiração, uso único)
7. **Sistema**: Altera senha
8. **Sistema**: Envia confirmação por email
9. **Usuário**: Faz login com nova senha

---

## ⚙️ Próximos Passos:

### Para Usar com Email Real:
1. Configurar conta de email (Gmail/SendGrid/SES)
2. Adicionar credenciais no `.env`
3. Descomentar linhas de envio de email no código
4. **REMOVER** `dev_code` da resposta da API
5. Testar fluxo completo

### Melhorias Futuras:
- [ ] Implementar rate limiting
- [ ] Adicionar captcha
- [ ] Histórico de alterações de senha
- [ ] Notificação de login suspeito
- [ ] 2FA opcional
- [ ] SMS como alternativa

---

## 🧪 Teste Rápido (Desenvolvimento):

1. Solicitar código: `POST /auth/request-reset-code` com `{"email": "user@test.com"}`
2. Ver código no console do backend ou na resposta
3. Validar código: `POST /auth/verify-reset-code` com:
```json
{
  "email": "user@test.com",
  "code": "123456",
  "new_password": "novaSenha123"
}
```

---

**Status Atual**: ✅ Funcionando em modo desenvolvimento (sem email configurado)
**Para Produção**: Configure email seguindo instruções acima
