from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def health(request):
    return JSONResponse({"status": "ok"})


def create_app() -> Starlette:
    return Starlette(
        debug=True,
        routes=[
            Route("/health", health),
        ],
    )


app = create_app()
