from fastapi import FastAPI
from backend.api.sample.controller import SampleController as sample
from backend.api.inference.onnx import OnnxController as onnx

app = FastAPI()
app.include_router(sample.router)
app.include_router(onnx.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"hello~!~! {name}"}
