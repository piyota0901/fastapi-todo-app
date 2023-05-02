#!/bin/bash
alias migrate='poetry run alembic upgrade head'
alias psql='docker exec -it postgresql15 psql --username todo_app --dbname tododb'