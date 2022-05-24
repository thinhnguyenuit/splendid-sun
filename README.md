### Splendid Suns

Splendid suns is a social blogging application written in Flask, a python framework.

Demo application: https://splendid-suns.herokuapp.com/

### Features
* User Authentication
* User Profile
* Blog Posts
* Comments (in the future)
* Likes (in the future)
* Followers (in the future)
* Unit Testing


### Installation

Initialize a virtual environment:

```commandline
pip íntall virtualenv
virtualenv venv
source venv/bin/activate
```

Install dependencies:

```commandline
pip install -r requirements.txt
```

Add the environment variable

```bash
SECRET_KEY=<your secret key>
DATABASE_URL=<your database url>
```

Run the database

```commandline
docker compose up
```

Run the server

```commandline
python run
```

Application will be available at: http://localhost:5000/
