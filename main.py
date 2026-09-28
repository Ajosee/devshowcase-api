from fastapi import FastAPI, Depends, HTTPException, status, Query, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

import models
import schemas
from database import engine, get_db

# 🌟 ATUALIZADO: Cria as tabelas diretamente no PostgreSQL do Supabase na nuvem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevShowcase API",
    description="Documentação interativa da API com tratamento global de erros e regras de negócio avançadas."
)

# ==========================================
# TRATAMENTO GLOBAL DE EXCEÇÕES (Erros 400, 404, etc)
# ==========================================

@app.exception_handler(HTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "sucesso": False,
            "erro": exc.status_code,
            "mensagem": exc.detail
        }
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    erros_formatados = []
    for erro in exc.errors():
        campo = " -> ".join([str(x) for x in erro["loc"] if x != "body"])
        erros_formatados.append(f"Campo '{campo}': {erro['msg']}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "sucesso": False,
            "erro": 400,
            "mensagem": "Erro de validação nos dados enviados.",
            "detalhes": erros_formatados
        }
    )

# ==========================================
# ENDPOINTS: PERFIL (Profile)
# ==========================================

@app.post("/api/profiles", response_model=schemas.Profile, status_code=status.HTTP_201_CREATED)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).filter(models.Profile.email == profile.email).first()
    if db_profile:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado em outro perfil.")
    
    new_profile = models.Profile(name=profile.name, bio=profile.bio, email=profile.email)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@app.get("/api/profiles/{id}", response_model=schemas.Profile)
def get_profile(id: int, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil buscado não foi encontrado no sistema.")
    return db_profile


# ==========================================
# ENDPOINTS: TECNOLOGIA (Technology)
# ==========================================

@app.post("/api/technologies", response_model=schemas.Technology, status_code=status.HTTP_201_CREATED)
def create_technology(tech: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    db_tech = db.query(models.Technology).filter(models.Technology.name == tech.name).first()
    if db_tech:
        raise HTTPException(status_code=400, detail="Esta tecnologia já está cadastrada.")
    
    new_tech = models.Technology(name=tech.name)
    db.add(new_tech)
    db.commit()
    db.refresh(new_tech)
    return new_tech

@app.get("/api/technologies", response_model=List[schemas.Technology])
def list_technologies(db: Session = Depends(get_db)):
    return db.query(models.Technology).all()


# ==========================================
# ENDPOINTS: PROJETO (Project)
# ==========================================

@app.post("/api/projects", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).filter(models.Profile.id == project.profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil associado ao projeto não foi encontrado.")
    
    new_project = models.Project(
        title=project.title,
        description=project.description,
        url=project.url,
        profile_id=project.profile_id,
        upvotes=0,
        average_rating=0.0
    )
    
    if project.technology_ids:
        db_techs = db.query(models.Technology).filter(models.Technology.id.in_(project.technology_ids)).all()
        new_project.technologies = db_techs

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@app.get("/api/projects", response_model=List[schemas.Project])
def list_projects(
    technology: Optional[str] = Query(None, description="Filtrar projetos por nome de tecnologia (ex: Python)"),
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(5, ge=1, le=50, description="Quantidade de projetos por página"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Project)
    if technology:
        query = query.join(models.Project.technologies).filter(models.Technology.name.ilike(f"%{technology}%"))
    
    skip = (page - 1) * limit
    projects = query.offset(skip).limit(limit).all()
    return projects

@app.put("/api/projects/{id}/upvote", response_model=schemas.Project)
def upvote_project(id: int, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Projeto informado para upvote não foi encontrado.")
    
    db_project.upvotes += 1
    db.commit()
    db.refresh(db_project)
    return db_project

@app.post("/api/projects/{id}/feedbacks", response_model=schemas.Feedback, status_code=status.HTTP_201_CREATED)
def create_project_feedback(id: int, feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Projeto informado para feedback não foi encontrado.")
    
    new_feedback = models.Feedback(
        comment=feedback.comment,
        rating=feedback.rating,
        project_id=id
    )
    db.add(new_feedback)
    db.commit()
    
    media_nota = db.query(func.avg(models.Feedback.rating)).filter(models.Feedback.project_id == id).scalar()
    db_project.average_rating = round(float(media_nota), 2) if media_nota else 0.0
    db.commit()
    
    db.refresh(new_feedback)
    return new_feedback
