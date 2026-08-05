from fastapi import FastAPI
app=FastAPI(title='CHIMERA Runtime')
@app.get('/health')
def health(): return {'status':'ok'}
