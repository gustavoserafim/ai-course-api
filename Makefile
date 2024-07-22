run_dev:
	DEBUG=true \
	MONGODB_URI=mongodb+srv://videoanalytics:21LnlX783j1qSK0@cluster0.oymj9jj.mongodb.net/ \
	TELA_URL=http://104.171.203.49:8000/ \
	OTEL_RESOURCE_ATTRIBUTES=service.name=YDUQS-PoC \
	OTEL_EXPORTER_OTLP_ENDPOINT="http://104.171.202.158:4317" \
	OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
	opentelemetry-instrument \
	uvicorn app.main:app --log-config app/log_config.json --reload