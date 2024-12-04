from fastapi import FastAPI
import uvicorn

app = FastAPI()

def read_root():
    return  {"Hello": "World"}

@app.get("/")
async def root():
    return {"message": "Hello to my HackCamp APP"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello  {name}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)