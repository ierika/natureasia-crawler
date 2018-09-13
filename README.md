# NatureAsia Crawler and Sitemap Generator

Crawls NatureAsia.com, stores the URLs in a database, and exports a sitemap XML.
It does not follow through non-NatureAsia URLs, but will record redirects from a NatureAsia URL,
but it does not go deeper than that.
Uses Scrapy, a Python module.

## Requirements
- Python 3
- Internet connection

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
`which python3` ensures the virtualenv will use a Python3 executable, not the ver. 2.

Enable virtual environment by sourcing it.
```bash
$ source venv/bin/activate
```
To deactivate (after you're done with using the app)
```bash
$ deactivate
```

### Install dependencies

```bash
$ pip install -r requirements.txt
```


## How to use
### Switch to virtual environment
```bash
$ cd /path/to/cloned/project
$ source venv/bin/activate
```
### Run crawl script
```bash
$ python main.py
```

### Run crawl script in the background (optional but recommended)
If you want to run it in the background and monitor the output
```bash
$ nohup python main.py &
```

NOTE: This will just update the current database that has been created.
`nohup.out` (**nohup** means no hangup) will be generated on the directory you ran it from.
It will contain the output of the program in which you can monitor anytime.

To monitor the output:
```bash
$ tail -f nohup.out
```


### Database output location
The crawler script will write to an Sqlite database while it's running.
That database is located at `exports/urls.db`.


## Browse the database
If you're not familiar with `sqlite3` commands. Please consider installing a desktop application.

https://sqlitebrowser.org/


### Export XML file
At the same directory where `main.py` is, run the following command:
```bash
$ python export_xml.py
```

XML file output location:
`exports/sitemap_<current_datetime>.xml`

If the number of URLs to be generated exceeds 50,000, the script will
separate the URLs into several XML files. Each containing a maximum of 50k URLs.
