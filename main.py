import uvicorn

if __name__ == "__main__":
    uvicorn.run("frameworks_drivers.fastapi_main:app", host="0.0.0.0", port=8000, reload=True)
