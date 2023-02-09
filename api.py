from typing import List
from async_google_trans_new import AsyncTranslator
# import databases
# import sqlalchemy
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import asyncio
from fastapi.responses import FileResponse



# # SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./test.db"
# # DATABASE_URL = "postgresql://user:password@postgresserver/db"

# database = databases.Database(DATABASE_URL)

# metadata = sqlalchemy.MetaData()

# notes = sqlalchemy.Table(
#     "notes",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("text", sqlalchemy.String),
#     sqlalchemy.Column("completed", sqlalchemy.Boolean),
# )


# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )
# metadata.create_all(engine)



class TranslateIn(BaseModel):
    text: str
    dest: str
    src: str



class Note(BaseModel):
    id: int
    text: str
    completed: bool


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


# @app.get("/notes/", response_model=List[Note])
# async def read_notes():
#     query = notes.select()
#     return await database.fetch_all(query)


# @app.post("/notes/", response_model=Note)
# async def create_note(note: NoteIn):
#     query = notes.insert().values(text=note.text, completed=note.completed)
#     last_record_id = await database.execute(query)
#     return {**note.dict(), "id": last_record_id}



@app.post("/translate/")
async def create_note(form: TranslateIn):
    try:
        
        datadict = {**form.dict()}
        data = datadict["text"]
        dest = datadict["dest"]
        g = AsyncTranslator()
        texts = [content for content in data.split("\n")]
        gathers = []
        for text in texts:
            gathers.append(g.translate(text, dest))

        a = await asyncio.gather(*gathers)
        html = "\n".join([i.replace(r"\ n", "\n").replace(r"\ t", "\t") for i in a])
        return html
    except:
        return "Không dịch được"
    

# router này mở kết nối đến trang chủ
@app.get("/")
async def getk():
    return FileResponse("index.html")



@app.get("/api/traslate")
async def apiTraslate(form: TranslateIn):
    try:
        
        datadict = {**form.dict()}
        data = datadict["text"]
        dest = datadict["dest"]
        g = AsyncTranslator()
        texts = [content for content in data.split("\n")]
        gathers = []
        for text in texts:
            gathers.append(g.translate(text, dest))

        a = await asyncio.gather(*gathers)
        html = "\n".join([i.replace(r"\ n", "\n").replace(r"\ t", "\t") for i in a])
        return html
    except:
        return "Không dịch được"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=80, log_level="info",host="0.0.0.0")