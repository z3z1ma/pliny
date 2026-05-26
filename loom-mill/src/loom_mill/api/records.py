from pathlib import Path

from starlette.responses import JSONResponse

from loom_mill.state import MillStateStore


async def get_record_content(request):
    record_id = request.path_params["record_id"]
    store: MillStateStore = request.app.state.store
    snapshot = await store.snapshot()

    record = next((item for item in snapshot.records if item.metadata.id == record_id or item.path == record_id), None)
    if record is None:
        return JSONResponse({"detail": "Record not found"}, status_code=404)

    path = Path(request.app.state.workspace_root) / ".loom" / record.path
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return JSONResponse({"detail": "Record not found"}, status_code=404)

    return JSONResponse({"id": record_id, "path": record.path, "content": content})
