from fastapi import FastAPI
from models import Base
from database import engine
from routers import roles, employees, users, attendance, leaves, performance_reviews

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(roles.router, prefix="/roles", tags=["roles"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
app.include_router(leaves.router, prefix="/leaves", tags=["leaves"])
app.include_router(performance_reviews.router, prefix="/performance_reviews", tags=["performance_reviews"])