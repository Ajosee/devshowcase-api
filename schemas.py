from pydantic import BaseModel, HttpUrl, EmailStr, Field
from typing import List, Optional

# ==========================================
# SCHEMAS PARA TECNOLOGIA (Technology)
# ==========================================
class TechnologyBase(BaseModel):
    name: str = Field(..., min_length=1, description="O nome da tecnologia não pode ser vazio")

class TechnologyCreate(TechnologyBase):
    pass

class Technology(TechnologyBase):
    id: int

    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS PARA PERFIL (Profile)
# ==========================================
class ProfileBase(BaseModel):
    name: str = Field(..., min_length=1, description="O nome não pode ser vazio")
    bio: Optional[str] = None
    email: EmailStr  # Valida automaticamente se o e-mail tem formato correto (ex: nome@email.com)

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS PARA PROJETO (Project)
# ==========================================
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, description="O título não pode ser vazio")
    description: Optional[str] = None
    url: str  # Armazena a URL enviada pelo usuário

class ProjectCreate(ProjectBase):
    profile_id: int
    technology_ids: List[int] = []  # Lista de IDs das tecnologias usadas no projeto

class Project(ProjectBase):
    id: int
    profile_id: int
    technologies: List[Technology] = []

    class Config:
        from_attributes = True
