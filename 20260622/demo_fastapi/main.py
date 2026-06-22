from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name:str
    age:int

# 라우터  (사용자의 특별한 url을 입력하면 해당 url에 맞는 함수를 실행해서 결과를 리턴하면) 
# 서버를 호출한 클라이언트(브라우져)에게 전달

@app.get("/")
def root():
    return {"message":"hello fastapi"}

@app.get("/msg")
def msg():
    return {"message":"good"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
# uvicorn main:app  --reload