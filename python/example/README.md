# Sample Python Project

This project uses Nix to provide a reproducible development environment.

## Getting Started

To get started with this project, you need to have Nix installed.

1.  **Enter the development environment:**
    ```bash
    nix-shell
    ```
    This command will set up a shell with Python 3.13, pip, and other necessary tools. It will also:
    *   Create a Python virtual environment (`.venv`) if it doesn't already exist.
    *   Install all dependencies listed in `requirements.txt` into the virtual environment.
    *   Source the `.env` file if present, exporting its variables.

2.  **Environment Variables:**
    Ensure you have a `.env` file in the project root for environment-specific configurations. An example file, `.env.example`, is provided.

## Development

To run the FastAPI application in development mode with auto-reloading:

```bash
fastapi dev main.py
```

## Production

To run the FastAPI application in production mode:

```bash
fastapi run main.py
```

## Running Tests

To execute the project's tests:

```bash
pytest
```
