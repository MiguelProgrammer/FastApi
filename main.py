from fastapi import FastAPI

from api.v1.api import api_router
from core.configs import settings

app = FastAPI(title="FastApi - Security")
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
    
    
    """_summary_
    TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzUxNzU0OTg5LCJpYXQiOjE3NTExNTAxODksInN1YiI6IjgifQ.BxZbw5k23Eh1CX9t1o8s101Yj-tVSVdaU5ERssv50M0
    TIPO: Bearer
    
    """