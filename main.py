from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# Cria automaticamente as tabelas no arquivo SQLite (devshowcase.db) ao iniciar a aplicação
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevShowcase API")

# ==========================================
# ENDPOINTS: PERFIL (Profile)
# ==========================================

@app.post("/api/profiles", response_model=schemas.Profile, status_code=status.HTTP_201_CREATED)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    # Verifica se já existe um perfil cadastrado com o mesmo e-mail
    db_profile = db.query(models.Profile).filter(models.Profile.email == profile.email).first()
    if db_profile:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado em outro perfil.")
    
    # Cria o novo registro no banco de dados
    new_profile = models.Profile(name=profile.name, bio=profile.bio, email=profile.email)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@app.get("/api/profiles/{id}", response_model=schemas.Profile)
def get_profile(id: int, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return db_profile


# ==========================================
# ENDPOINTS: TECNOLOGIA (Technology)
# ==========================================

@app.post("/api/technologies", response_model=schemas.Technology, status_code=status.HTTP_201_CREATED)
def create_technology(tech: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    # Evita duplicar tecnologias com o mesmo nome
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
    # Verifica se o perfil informado realmente existe no banco
    db_profile = db.query(models.Profile).filter(models.Profile.id == project.profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil associado ao projeto não foi encontrado.")
    
    # Monta a estrutura inicial do projeto
    new_project = models.Project(
        title=project.title,
        description=project.description,
        url=project.url,
        profile_id=project.profile_id
    )
    
    # Busca no banco e vincula as tecnologias enviadas por ID
    if project.technology_ids:
        db_techs = db.query(models.Technology).filter(models.Technology.id.in_(project.technology_ids)).all()
        new_project.technologies = db_techs

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@app.get("/api/projects", response_model=List[schemas.Project])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()
