# NatureAsia Crawler and Sitemap Generator

Crawls NatureAsia.com, stores the URLs in a database, and exports a sitemap XML.
It does not follow through non-NatureAsia URLs, but will record redirects from a NatureAsia URL,
but it does not go deeper than that.
Uses Scrapy, a Python module.

## Requirements
- Python 3
- Internet connection (duh!)


## Installation

### Install Python 3
On Mac
```bash
$ brew install python3
```
On Linux
```bash
$ sudo apt-get update
$ sudo apt-get install python3.6
```

### Install VirtualEnv
```bash
$ python3 -m pip install virtualenv
```

### Clone this project and make a virtual environment for this project to run on
```bash
$ cd /path/to/cloned/project
$ virtualenv venv --python=$(which python3)
```

Enable virtual environment by sourcing it.
```bash
$ source venv/bin/activate
```
To deactivate (after you're done with using the app)
```bash
$ deactivate
```

`which python3` ensures the virtualenv will use a Python3 executable, not the ver. 2.

### Install dependencies

```bash
$ pip install -r requirements.txt
```


## How to use
```bash
$ python src/main.py
```
If you want to run it in the background
```bash
$ nohup python src/main.py &
```
This will just update the current database that has been created.

`nohup.out` will be generated on the directory you ran it from.
It will contain the output of the program.

## Output
The program will be outputting two files. One is the database and the other one
is the XML file, the sitemap.

Database output location:
`src/urls.db`

XML file output location:
`~/Downloads/sitemap_<current_datetime>.xml`


## Browse the database
If you're not familiar with `sqlite3` commands. Please consider installing a desktop application.

https://sqlitebrowser.org/
