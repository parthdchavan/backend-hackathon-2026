from fastapi import FastAPI, Depends
from database import engine, get_db, Base
from auth import verify_token
from llm import query_llm
from models import Agent, Log, Objection
from sqlalchemy.orm import Session
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hapticware Mini AI Agent Monitor")

@app.get("/")
def root():
    return {"message": "API running 🚀"}

@app.get("/test-db")
def test_db():
    try:
        conn = engine.connect()
        conn.close()
        return {"message": "DB connected successfully ✅"}
    except Exception as e:
        return {"error": str(e)}

# --- Agents ---

class AgentCreate(BaseModel):
    name: str

@app.post("/agents", dependencies=[Depends(verify_token)])
def create_agent(body: AgentCreate, db: Session = Depends(get_db)):
    agent = Agent(name=body.name)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@app.get("/agents", dependencies=[Depends(verify_token)])
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()

# --- Logs ---

class LogCreate(BaseModel):
    message: str
    level: str = "info"

@app.post("/agents/{agent_id}/logs", dependencies=[Depends(verify_token)])
def add_log(agent_id: int, body: LogCreate, db: Session = Depends(get_db)):
    log = Log(agent_id=agent_id, message=body.message, level=body.level)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@app.get("/agents/{agent_id}/logs", dependencies=[Depends(verify_token)])
def get_logs(agent_id: int, db: Session = Depends(get_db)):
    return db.query(Log).filter(Log.agent_id == agent_id).all()

# --- Objections ---

class ObjectionCreate(BaseModel):
    text: str

@app.post("/objections", dependencies=[Depends(verify_token)])
def create_objection(body: ObjectionCreate, db: Session = Depends(get_db)):
    obj = Objection(text=body.text)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/objections", dependencies=[Depends(verify_token)])
def list_objections(db: Session = Depends(get_db)):
    return db.query(Objection).order_by(Objection.created_at.desc()).all()

# --- LLM ---

class LLMQuery(BaseModel):
    prompt: str

@app.post("/llm/query", dependencies=[Depends(verify_token)])
def llm_query(body: LLMQuery):
    result = query_llm(body.prompt)
    return {"response": result}
