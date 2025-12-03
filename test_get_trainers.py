from database import get_db
from users import user_service


def run():
    db = next(get_db())
    try:
        trainers = user_service.get_approved_trainers(db)
        print(f"Found trainers: {len(trainers)}")
        for t in trainers:
            print(t)
    finally:
        db.close()

if __name__ == '__main__':
    run()
