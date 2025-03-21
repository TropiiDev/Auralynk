import random

from fastapi import HTTPException
from functions import *
from sql import *

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Welcome to Auralynk"}

@app.post("/user/create", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    salt = random.randint(00000, 99999)
    existing_user = session.query(MainUser).filter(MainUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = hash_password(user.password, salt)
    user.salt = salt

    db_user = MainUser.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/user/", response_model=UserPublic)
def get_user(user: VerifyUser, session: SessionDep):
    existing_user = session.query(MainUser).filter(MainUser.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Email not registered")
    return existing_user

@app.get('/user/verify')
async def verify_user(user: VerifyUser, session: SessionDep):
    existing_user = session.query(MainUser).filter(MainUser.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Email not registered")

    is_password_valid = validate_password(user.password, existing_user.password, existing_user.salt)

    if not is_password_valid:
        raise HTTPException(status_code=400, detail="Password not valid")

    return {"is_password_valid": is_password_valid, "email": existing_user.email, "id": existing_user.id}

@app.patch("/user/update/{user_id}", response_model=UserPublic)
async def update_user(user_id: int, user: UpdateUser, session: SessionDep):
    user_db = session.get(MainUser, user_id)
    user_data = user.model_dump(exclude_unset=True)

    if 'songs' in user_data:
        if user_db.songs is None:
            user_db.songs = []
        current_songs = user_db.songs
        new_songs = user_data['songs']
        user_data['songs'] = current_songs + new_songs

    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db
