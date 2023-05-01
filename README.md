# Linkta
**Linkta** is a web application to put all your links in a single page.

## Install:

Make sure you have latest python installed

Clone the repository

> clone with HTTP
```
git clone https://github.com/biswarupmurmu/Linkta.git
```

> or clone with SSH

```
git clone git@github.com:biswarupmurmu/Linkta.git
```

Go inside the project directory

```
cd Linkta
```

Create a virtual environment and activate it

```
python3 -m venv env
. env/bin/activate
```

Or on Windows cmd

```
python -m venv env
env\Scripts\activate.bat
```

Install **Linkta**

```
pip install -e .
```

## Run:

```
flask --app linkta init-db
flask --app linkta run --debug
```

Open http://127.0.0.1:5000 in a browser.

## Framework used

> ## Flask