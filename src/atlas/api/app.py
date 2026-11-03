from __future__ import annotations

from fastapi import FastAPI, HTTPException


def create_app() -> FastAPI:
    app = FastAPI(title="ATLAS Genesis", version="0.1.0")

    @app.get("/api/v1/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/api/v1/chat")
    def chat() -> None:
        # TODO(fase 1): autenticar, clasificar datos y delegar en CognitiveCore.handle
        raise HTTPException(status_code=501, detail="no implementado")

    return app


app = create_app()
