import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.main:app",
                port=8080,
                reload=True,
                ssl_keyfile="./src/security/key.pem", 
                ssl_certfile="./src/security/cert.pem"
                )