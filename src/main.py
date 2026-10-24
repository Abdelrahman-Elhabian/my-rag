from fastapi import FastAPI
from routes import base, data

app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)

@app.get("/")
@app.get("/welcome")
async def root_welcome(app_settings: base.Settings = base.Depends(base.get_settings)):
    return await base.welcome(app_settings)

