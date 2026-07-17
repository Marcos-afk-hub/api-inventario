from fastapi import FastAPI

#Now we create an instance to our application  

app = FastAPI(
    title="Inventory API",
    description="API REST to inventory products management",
    version="0.1.0"
)

#First PATH
@app.get("/")
def root ():
    return {"message": "¡Welcome to Inventory API!"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-inventario"}