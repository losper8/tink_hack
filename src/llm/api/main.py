from fastapi import FastAPI
from starlette.responses import RedirectResponse

from starlette.middleware.cors import CORSMiddleware
from giga_chat.api.giga_chat_router import giga_chat_router


def configure_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app = FastAPI(
    debug=True,
    title='Giga Chat',
)

configure_cors(app)

@app.get("/", include_in_schema=False)
async def redirect_from_root() -> RedirectResponse:
    return RedirectResponse(url='/docs')


app.include_router(giga_chat_router)
