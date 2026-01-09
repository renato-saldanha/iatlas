from fastapi import FastAPI
from typing import Dict
from datetime import datetime, timezone

app = FastAPI(
    title="IAtlas API",
    description="API REST de agente IA para auxilio nos estudos e análise de documentos",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Endpoint de health check para monitoramento de saúde da API
    Usado pelo Flyio para verificar se a aplicação está rodando.
    """

    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
