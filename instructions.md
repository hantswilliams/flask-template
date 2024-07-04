# Instructions 

## Run locally 
- Setup a virtual environment
    - `python3 -m venv venv` then `source venv/bin/activate`
    - Or if using VSCode, can just select the interpreter and let it create the venv and activate it for you
- Install NPM for the frontend
    - Following instructions from https://github.com/themesberg/tailwind-flask-starter
- To then monitor the changes, will need to have another terminal open with this running: 
```bash
npx tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/css/output.css --watch
```
- Then in another terminal, can first do: 
    - `python populate_db.py` to populate the database
    - `python app.py` to run the app

## To then build:

### Part 1:
```bash
docker build -t flask-tailwind-app .
```

### Part 2:
```bash
docker run -p 5027:5027 flask-tailwind-app
```