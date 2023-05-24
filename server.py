import uvicorn

def start_server():
    uvicorn.run(
        "main:get_app",
        host='127.0.0.1',
        port=8000,
        reload=True,
        factory=True
    )

if __name__ == '__main__':
    start_server()