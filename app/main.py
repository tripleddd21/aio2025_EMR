from fastapi import FastAPI
from app.routers import patients, visits, medical_history, search

app = FastAPI()
app.include_router(patients.router)
app.include_router(visits.router)
app.include_router(medical_history.router)
app.include_router(search.router)


for route in app.routes:
    print(route.path)
