import pytest

def test_ingestion_respects_config_structure(ingestion_instance):
    assert hasattr(ingestion_instance, "ingest")
    assert callable(getattr(ingestion_instance, "ingest"))

