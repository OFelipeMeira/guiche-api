

import fastapi
import pymysql
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel



def conecta():
    cnx = pymysql.connect(
        user="butterfly@peixe", password="Manteigavoadora1", host="peixe.mariadb.database.azure.com", port=3306,
        database="secretariasenai"
    )
    cursor = cnx.cursor()

    return cursor, cnx

cursor, cnx = conecta()


app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get")
def bd():
    cursor, cnx = conecta()
    cursor.execute("SELECT name FROM espera WHERE ja_atendido = 0 ORDER BY id ASC")
    values = cursor.fetchall()
    cnx.close()
    cursor.close()
    return {"message": values}


class request(BaseModel):
    guiche: int

@app.post("/post")
def post(a: request):
    cursor, cnx = conecta()
    cursor.execute("SELECT id FROM espera WHERE ja_atendido = 0 ORDER BY id ASC")
    values = cursor.fetchall()
    val0 = values[0][0]
    cursor.execute(f"UPDATE espera SET guiche = {a.guiche}, ja_atendido = 1 WHERE id = {val0}")
    cursor.execute(f"SELECT name, motivo FROM espera WHERE id = {val0}")
    values = cursor.fetchall()
    cnx.commit()
    cnx.close()
    cursor.close()
    return {"message": values[0]}