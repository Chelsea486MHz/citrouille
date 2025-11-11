import json
from datetime import datetime
from citrouille.formatters import TableFormatter, JSONFormatter


class TestTableFormatter:
    def test_format_empty_deployments(self):
        deployments = []
        result = TableFormatter.format_deployments(deployments)
        assert result == "No deployments found."

    def test_format_single_deployment(self):
        deployments = [{
            "name": "nginx",
            "namespace": "default",
            "images": ["nginx:1.21"],
            "created": datetime(2024, 11, 11, 10, 30, 0),
            "replicas": 3
        }]
        result = TableFormatter.format_deployments(deployments)
        assert "NAME" in result
        assert "NAMESPACE" in result
        assert "IMAGES" in result
        assert "CREATED" in result
        assert "REPLICAS" in result
        assert "nginx" in result
        assert "default" in result
        assert "nginx:1.21" in result
        assert "2024-11-11" in result
        assert "3" in result

    def test_format_multiple_deployments(self):
        deployments = [
            {
                "name": "nginx",
                "namespace": "default",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3
            },
            {
                "name": "redis",
                "namespace": "cache",
                "images": ["redis:7.0"],
                "created": datetime(2024, 11, 10, 15, 45, 0),
                "replicas": 1
            }
        ]
        result = TableFormatter.format_deployments(deployments)
        assert "nginx" in result
        assert "redis" in result
        assert "default" in result
        assert "cache" in result

    def test_format_deployment_with_multiple_images(self):
        deployments = [{
            "name": "app",
            "namespace": "production",
            "images": ["app:v1.0", "sidecar:v2.1", "logger:latest"],
            "created": datetime(2024, 11, 11, 10, 30, 0),
            "replicas": 5
        }]
        result = TableFormatter.format_deployments(deployments)
        assert "app:v1.0, sidecar:v2.1, logger:latest" in result

    def test_format_deployment_with_no_images(self):
        deployments = [{
            "name": "empty",
            "namespace": "default",
            "images": [],
            "created": datetime(2024, 11, 11, 10, 30, 0),
            "replicas": 0
        }]
        result = TableFormatter.format_deployments(deployments)
        assert "None" in result

    def test_format_deployment_with_none_timestamp(self):
        deployments = [{
            "name": "test",
            "namespace": "default",
            "images": ["test:latest"],
            "created": None,
            "replicas": 1
        }]
        result = TableFormatter.format_deployments(deployments)
        assert "Unknown" in result


class TestJSONFormatter:
    def test_format_empty_deployments(self):
        deployments = []
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert parsed == []

    def test_format_single_deployment(self):
        deployments = [{
            "name": "nginx",
            "namespace": "default",
            "images": ["nginx:1.21"],
            "created": datetime(2024, 11, 11, 10, 30, 0),
            "replicas": 3
        }]
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert len(parsed) == 1
        assert parsed[0]["name"] == "nginx"
        assert parsed[0]["namespace"] == "default"
        assert parsed[0]["images"] == ["nginx:1.21"]
        assert parsed[0]["replicas"] == 3
        assert "2024-11-11" in parsed[0]["created"]

    def test_format_multiple_deployments(self):
        deployments = [
            {
                "name": "nginx",
                "namespace": "default",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3
            },
            {
                "name": "redis",
                "namespace": "cache",
                "images": ["redis:7.0"],
                "created": datetime(2024, 11, 10, 15, 45, 0),
                "replicas": 1
            }
        ]
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert len(parsed) == 2
        assert parsed[0]["name"] == "nginx"
        assert parsed[1]["name"] == "redis"

    def test_format_deployment_with_none_timestamp(self):
        deployments = [{
            "name": "test",
            "namespace": "default",
            "images": ["test:latest"],
            "created": None,
            "replicas": 1
        }]
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert parsed[0]["created"] is None

    def test_json_is_valid(self):
        deployments = [{
            "name": "test",
            "namespace": "default",
            "images": ["test:latest"],
            "created": datetime(2024, 11, 11, 10, 30, 0),
            "replicas": 1
        }]
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert isinstance(parsed, list)
