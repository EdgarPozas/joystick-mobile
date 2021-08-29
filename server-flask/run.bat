$env:FLASK_ENV = "development"
flask run --no-debugger -h 0.0.0.0

$env:FLASK_ENV = "production"