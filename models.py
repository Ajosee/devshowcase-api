from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabela auxiliar para o relacionamento N:N (Muitos para Muitos) entre Project e Technology
project_technology = Table(
    'project_technology',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('technology_id', Integer, ForeignKey('technologies.id'), primary_key=True)
)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)

    # Relacionamento 1:N -> Um Perfil tem vários Projetos
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)

    # 🌟 NOVOS CAMPOS EXIGIDOS NA ETAPA 2:
    upvotes = Column(Integer, default=0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)

    # Relacionamentos ajustados e conectados
    profile = relationship("Profile", back_populates="projects")
    technologies = relationship("Technology", secondary=project_technology, back_populates="projects")
    feedbacks = relationship("Feedback", back_populates="project", cascade="all, delete-orphan")


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Volta do relacionamento N:N
    projects = relationship("Project", secondary=project_technology, back_populates="technologies")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    
    # 🌟 NOVO CAMPO DE NOTA DE 1 A 5 EXIGIDO NA ETAPA 2:
    rating = Column(Integer, nullable=False)
    
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

    # Volta do relacionamento 1:N
    project = relationship("Project", back_populates="feedbacks")
