from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uuid

from core.config import APP_NAME
from core.security import hashed_password, verify_password, create_access_token, decode_access_token
from database.database import engine, Base, SessionLocal
from database import model
from schemas.user import UserCreate, UserOut, LoginRequest, TokenResponse
from fastapi import UploadFile, File
import os
import shutil
from schemas.document import DocumentOut
from rag.pipeline import answer_query
from agent.agent import run_agent

Base.metadata.create_all(bind=engine)

app = FastAPI()
chat_history = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(model.User).filter(model.User.id == payload.get("sub")).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@app.get("/")
def read_root():
    return {"message": f"Hello from {APP_NAME}!"}


@app.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(model.User).filter(model.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = model.User(
        id=str(uuid.uuid4()),
        email=user_in.email,
        hashed_password=hashed_password(user_in.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=TokenResponse)
def login(user_in: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token(user.id)
    return TokenResponse(access_token=token)


@app.get("/me", response_model=UserOut)
def read_current_user(current_user: model.User = Depends(get_current_user)):
    return current_user


UPLOAD_DIR = "uploads"

@app.post("/documents/uploads", response_model = DocumentOut)
def upload_document(
    file : UploadFile = File(...),
    db : Session = Depends(get_db),
    current_user : model.User = Depends(get_current_user),
):
    os.makedirs(UPLOAD_DIR, exist_ok = True)
    safe_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb")as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_document = model.Document(
        id = str(uuid.uuid4()),
        owner_id = current_user.id,
        filename = file.filename,
        file_path = file_path,
        status = "uploaded"
    )   

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document

@app.get("/documents", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    return db.query(model.Document).filter(model.Document.owner_id == current_user.id).all()

@app.get("/chat")
def chat(query:str , current_user: model.User = Depends(get_current_user)):
   from rag.query_rewriter import rewrite_query

   user_id = current_user.id

   history = chat_history.get(user_id,[])

   standlone_query = rewrite_query(query,history)

   result = answer_query(standlone_query)

   history.append(query)

   chat_history[user_id] = history

   return result


@app.get("/agent-chat")
def agent_chat(query:str , current_user: model.User = Depends(get_current_user)):
     print(f"DEBUG: received query = '{query}'")
     return run_agent(query)