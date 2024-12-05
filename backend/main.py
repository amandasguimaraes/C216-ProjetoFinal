from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os

# Função para obter a conexão com o banco de dados PostgreSQL
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/doacao")
    return await asyncpg.connect(DATABASE_URL)

# Inicializar a aplicação FastAPI
app = FastAPI()

# Modelo para adicionar novos doadores
class Doador(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    telefone: str
    tipo_sanguineo: str
    data_nascimento: str
    endereco: str

# Modelo para adicionar novos receptores
class Receptor(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    telefone: str
    tipo_sanguineo: str
    data_nascimento: str
    endereco: str
    necessidade_sangue: bool

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

# 1. Adicionar um novo doador
@app.post("/api/v1/doadores/", status_code=201)
async def adicionar_doador(doador: Doador):
    conn = await get_database()
    try:
        query = """
        INSERT INTO doadores (nome, email, telefone, tipo_sanguineo, data_nascimento, endereco)
        VALUES ($1, $2, $3, $4, $5, $6)
        """
        async with conn.transaction():
            await conn.execute(
                query, 
                doador.nome, doador.email, doador.telefone, doador.tipo_sanguineo, 
                doador.data_nascimento, doador.endereco
            )
        return {"message": "Doador adicionado com sucesso!"}
    finally:
        await conn.close()

# 2. Listar todos os doadores
@app.get("/api/v1/doadores/", response_model=List[Doador])
async def listar_doadores():
    conn = await get_database()
    try:
        query = "SELECT * FROM doadores"
        rows = await conn.fetch(query)
        doadores = [dict(row) for row in rows]
        return doadores
    finally:
        await conn.close()

# 3. Adicionar um novo receptor
@app.post("/api/v1/receptores/", status_code=201)
async def adicionar_receptor(receptor: Receptor):
    conn = await get_database()
    try:
        query = """
        INSERT INTO receptores (nome, email, telefone, tipo_sanguineo, data_nascimento, endereco, necessidade_sangue)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        """
        async with conn.transaction():
            await conn.execute(
                query, 
                receptor.nome, receptor.email, receptor.telefone, receptor.tipo_sanguineo, 
                receptor.data_nascimento, receptor.endereco, receptor.necessidade_sangue
            )
        return {"message": "Receptor adicionado com sucesso!"}
    finally:
        await conn.close()

# 4. Listar todos os receptores
@app.get("/api/v1/receptores/", response_model=List[Receptor])
async def listar_receptores():
    conn = await get_database()
    try:
        query = "SELECT * FROM receptores"
        rows = await conn.fetch(query)
        receptores = [dict(row) for row in rows]
        return receptores
    finally:
        await conn.close()

# 5. Atualizar a necessidade de sangue de um receptor
@app.patch("/api/v1/receptores/{receptor_id}")
async def atualizar_necessidade_sangue(receptor_id: int, necessidade_sangue: bool):
    conn = await get_database()
    try:
        query = "UPDATE receptores SET necessidade_sangue = $1 WHERE id = $2"
        await conn.execute(query, necessidade_sangue, receptor_id)
        return {"message": "Necessidade de sangue atualizada com sucesso!"}
    finally:
        await conn.close()

# Resetar banco de dados
@app.delete("/api/v1/reset-database/")
async def reset_database():
    init_sql_path = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        with open(init_sql_path, "r") as file:
            sql_commands = file.read()
        
        await conn.execute(sql_commands)
        return {"message": "Banco de dados resetado com sucesso!"}
    finally:
        await conn.close()
