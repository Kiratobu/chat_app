## Description
Real-time chat application


This app uses:
- Python FastAPI+WebSockets [docs](https://fastapi.tiangolo.com/)
- MongoDB [docs](https://docs.mongodb.com/manual/)
- Docker [docs](https://docs.docker.com/engine/reference/run/)

## Setting up and running

Creating .env file with variables: 
- MONGO_PORT=27017
- MONGO_USER=user_1
- MONGO_PASS=some_pass
- MONGO_DB=db_chat

- SECRET=SECRET


Run docker container:

<b>docker-compose -f   docker-compose.yml up -d --build</b>

Link for docs: 
<b>http://localhost:8000/docs/</b>

For using Websockets creating new User, new Room and append new User to Room.
