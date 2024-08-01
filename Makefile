run_dev:
	DEBUG=true \
	MONGODB_URI=mongodb+srv://videoanalytics:21LnlX783j1qSK0@cluster0.oymj9jj.mongodb.net/ \
	TELA_MOTOR_A_URL="http://104.171.203.212:8000" \
	TELA_MOTOR_B_URL="http://104.171.203.212:8081" \
	OTEL_RESOURCE_ATTRIBUTES="service.name=yduqs-poc-local" \
	OTEL_EXPORTER_OTLP_ENDPOINT="http://104.171.202.158:4317" \
	OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
	opentelemetry-instrument \
	uvicorn app.main:app --log-config app/log_config.json --reload