from fastapi import FastAPI

app = FastAPI()


@app.geet("/")
def root():
    return {"message": "Hello"}


@app.get("/api/health")
def health():
    return {"ok": True}
