# local
~/Desktop/code/fastapi-todo-app $ python3 -m venv venv                                                                                                                                                                          ──(土,1012)─┘

~/Desktop/code/fastapi-todo-app $ source venv/bin/activate  # Linux/Mac                                                                                                                                                         ──(土,1012)─┘


# docker
docker build -t fastapi-app .
docker run -d --name fastapi-container -p 8000:8000 fastapi-app


# test
pytest --cov=app tests/

![Test Image](./test_result.png)


# other
swaggerUI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc
