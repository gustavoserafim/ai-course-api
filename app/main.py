from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.api.endpoints import websocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.websocket import manager as ws

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

tracer = trace.get_tracer(__name__)

def configure_opentelemetry(app: FastAPI):
    trace.set_tracer_provider(TracerProvider())
    span_processor = BatchSpanProcessor(
        OTLPSpanExporter(
            insecure=True,
        )
    )
    trace.get_tracer_provider().add_span_processor(span_processor)
    FastAPIInstrumentor.instrument_app(app)

configure_opentelemetry(app)

app.include_router(api_router, prefix="/api")
app.include_router(websocket.router, tags=["websockets"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {
        "message": "Welcome to the YDUQS AI API!"
    }

@app.get("/ping")
async def ws_ping():
    await ws.broadcast("Pong!")
    return {
        "message": "Sending ping to all clients."
    }