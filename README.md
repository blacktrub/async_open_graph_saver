## Simple Open Graph saver
It's simple implementation of asynchronous API for save Open Graph tags.

For start project you need next steps:

Create virtualenv
```
virtualenv -p python3 env
```

Activate it
```commandline
source env/bin/activate
```

Install all dependencies of project
```commandline
pip install -r requirements.txt
```

Create database and table
```postgresql
CREATE DATABASE open_graph_links OWNER 'admin';

CREATE TABLE links(
  id serial PRIMARY KEY, 
  url text, 
  title text, 
  description text, 
  image text);
```

Also you can set own settings of database in settings.py module

And now you may run server
```commandline
python server.py
```
