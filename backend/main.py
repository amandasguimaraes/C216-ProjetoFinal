from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
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
    data_nascimento: datetime
    endereco: str

class Doacoes(BaseModel):
    id: Optional[int] = None
    nome_doador: str
    tipo_sanguineo: str
    data_doacao: datetime

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


# 3. Buscar doador por ID
@app.get("/api/v1/doadores/{doador_id}")
async def listar_doadores_por_id(doador_id: int):
    conn = await get_database()
    try:
        # Buscar o doador por ID
        query = "SELECT * FROM doadores WHERE id = $1"
        doador = await conn.fetchrow(query, doador_id)
        if doador is None:
            raise HTTPException(status_code=404, detail="Doador não encontrado.")
        return dict(doador)
    finally:
        await conn.close()

# 4. Remover um doador pelo ID
@app.delete("/api/v1/doadores/{doador_id}")
async def remover_doador(doador_id: int):
    conn = await get_database()
    try:
        # Verificar se o doador existe
        query = "SELECT * FROM doadores WHERE id = $1"
        doador = await conn.fetchrow(query, doador_id)
        if doador is None:
            raise HTTPException(status_code=404, detail="Doador não encontrado.")
        # Remover o doador do banco de dados
        delete_query = "DELETE FROM doadores WHERE id = $1"
        await conn.execute(delete_query, doador_id)
        return {"message": "Doador removido com sucesso!"}
    finally:
        await conn.close()

@app.post("/api/v1/doadores/{doador_id}/doar/")
async def adicionar_doacao(doador_id: int, doacao: Doacoes):
    conn = await get_database()
    try:
        # Verificar se o doador existe
        query = "SELECT * FROM doadores WHERE id = $1"
        doador = await conn.fetchrow(query, doador_id)
        if doador is None:
            raise HTTPException(status_code=404, detail="Doador não encontrado.")
        data_doacao = datetime.now()
        # Registrar a doacao na tabela de doacoes
        insert_doacao_query = """
            INSERT INTO doacoes (nome_doador, tipo_sanguineo, data_doacao) 
            VALUES ($1, $2, $3)
        """
        await conn.execute(insert_doacao_query, doacao.nome_doador, doacao.tipo_sanguineo, data_doacao)
        return {"message": "Doação realizada com sucesso!"}
    finally:
        await conn.close()

@app.get("/api/v1/doacoes/")
async def listar_doacoes():
    conn = await get_database()
    try:
        # Buscar todas as doacoes no banco de dados
        query = "SELECT * FROM doacoes"
        rows = await conn.fetch(query)
        doacoes = [dict(row) for row in rows]
        return doacoes
    finally:
        await conn.close()

# Resetar banco de dados
@app.delete("/api/v1/reset-database/")
async def reset_database():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        with open(init_sql, "r") as file:
            sql_commands = file.read()
        
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()
