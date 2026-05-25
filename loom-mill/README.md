# Loom Mill

Minimal Factory Floor scaffold for the Loom Mill MVP.

## Development

Install backend dependencies from the repository root:

```bash
python -m venv loom-mill/.venv
source loom-mill/.venv/bin/activate
pip install -e loom-mill
```

Install frontend dependencies:

```bash
npm --prefix loom-mill/frontend install
```

Start the backend and frontend dev servers together:

```bash
npm run dev:mill
```

The root dev script uses `loom-mill/.venv/bin/python`, so run the backend install step before starting the stack.

Backend health check: `http://127.0.0.1:8765/health`

Frontend dev server: `http://127.0.0.1:5173`
