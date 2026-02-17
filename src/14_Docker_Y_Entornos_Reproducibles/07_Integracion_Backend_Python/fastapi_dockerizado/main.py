from fastapi import FastAPI
import os

app = FastAPI(title="FastAPI Dockerizado")

@app.get("/")
async def root():
    return {
        "message": "Hola desde un contenedor Docker!",
        "env": os.getenv("APP_ENV", "development"),
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
