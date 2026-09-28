from pydantic import BaseModel, Field, EmailStr
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
    email: EmailStr  # Valida automaticamente se o e-mail tem formato correto

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS PARA FEEDBACK / OPINIÃO (Feedback)
# ==========================================
class FeedbackBase(BaseModel):
    comment: str = Field(..., min_length=1, description="O comentário não pode ser vazio")
    # 🌟 VALIDAÇÃO EXIGIDA: Garante nota de 1 a 5 (ge = Greater or Equal / le = Less or Equal)
    rating: int = Field(..., ge=1, le=5, description="A nota deve ser um número inteiro entre 1 e 5")

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    project_id: int

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
    technology_ids: List[int] = []  # Lista de IDs das tecnologias usadas

class Project(ProjectBase):
    id: int
    profile_id: int
    
    # 🌟 NOVOS CAMPOS EXIGIDOS NA ETAPA 2 RETORNADOS NA SAÍDA:
    upvotes: int = 0
    average_rating: float = 0.0
    
    technologies: List[Technology] = []
    feedbacks: List[Feedback] = []  # Lista as opiniões vinculadas ao projeto

    class Config:
        from_attributes = True
