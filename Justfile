# default: list available recipes
default:
    @just --list

# run all tests
test:
    uv run pytest tests/ -v

# run the app locally
run:
    uv run uvicorn src.main:app --reload --port 8000

# build and run with docker
docker:
    docker compose up --build
