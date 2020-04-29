# Python Asynchronous I/O (asyncio)
> Using asyncio streams to emulate live sport games updates

Project consists of two parts: 
 - A data feed which emulates some source of real-time sport updates
 - A server application that connects to data feed and broadcasts the updates to a number of clients using websockets. Built using [FastAPI](https://fastapi.tiangolo.com/) framework 

## Installation

```sh
cp env.ini.dist env.ini
pipenv install
```

## Usage

Running the feed
```sh
pipenv run python feed.py --host 127.0.0.1 --port 5000 --count 10
```

Running the application
```sh
pipenv run uvicorn app:app --reload
```

For a live demo visit the [link](https://asyncio.viktors.info)
