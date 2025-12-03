from database import SessionLocal
from users.user_models import User
from roles.role_model import Role
from security import get_password_hash


def main():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == 'tester_trainer@example.com').first()
        if existing:
            print(f'Já existe trainer de teste: id={existing.id}, email={existing.email}')
            return

        role = db.query(Role).filter(Role.name == 'personal').first()
        if not role:
            role = Role(name='personal')
            db.add(role)
            db.commit()
            db.refresh(role)
            print(f'Role personal criado id={role.id}')

        hashed = get_password_hash('senha12345')
        new = User(
            email='tester_trainer@example.com',
            hashed_password=hashed,
            full_name='Tester Trainer',
            profile_image_url=None,
            approved=True,
            goals=None,
            fitness_level=None,
            registration_date=None,
            specialty='Força',
            cref=None,
            experience='5 anos',
            bio='Trainer de teste',
            hourly_rate='50',
            city='Cidade Teste',
            role_id=role.id
        )
        db.add(new)
        db.commit()
        db.refresh(new)
        print(f'Trainer criado com id={new.id}, email={new.email}')
    except Exception as e:
        print('Erro ao criar trainer de teste:', e)
    finally:
        db.close()


if __name__ == '__main__':
    main()
