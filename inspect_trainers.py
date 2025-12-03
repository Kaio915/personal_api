from database import SessionLocal
from users import user_repository


def main():
    db = SessionLocal()
    try:
        trainers = user_repository.get_approved_trainers(db)
        print('Found trainers:', len(trainers))
        for t in trainers:
            try:
                print(' -', t.id, getattr(t, 'email', None), getattr(t, 'full_name', None), 'role_id=', getattr(t, 'role_id', None), 'approved=', getattr(t, 'approved', None))
            except Exception as e:
                print('Error printing trainer:', e)
    except Exception as e:
        print('Error querying DB:', e)
    finally:
        db.close()

if __name__ == '__main__':
    main()
