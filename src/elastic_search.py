from elasticsearch import Elasticsearch

from src import config

# Elasticsearch 클라이언트 설정
es = Elasticsearch(
    [f"https://{config.elasticsearch.host}:{config.elasticsearch.port}"],
    basic_auth=(config.elasticsearch.id, config.elasticsearch.password),
    verify_certs=config.elasticsearch.verify_ssl,  # SSL 인증서 검증 비활성화
)
