# Name of the Docker image
IMAGE_NAME=mlops-core

# Default plugin name (can be overridden)
PLUGIN ?= fmp

# Config file to mount (defaults to example_config_<plugin>.yaml)
CONFIG_FILE ?= example_config_$(PLUGIN).yaml

# Paths
PLUGINS_DIR = $(PWD)/plugins
TEST_PLUGINS_DIR = $(PWD)/tests/test_plugins
CONFIG_PATH = $(PWD)/$(CONFIG_FILE)

# Rebuild the Docker image from scratch
build:
	docker build --no-cache -t $(IMAGE_NAME) .

# Run tests for the selected plugin
test-plugin:
	docker run --rm \
	  -v $(PLUGINS_DIR):/app/plugins \
	  -v $(TEST_PLUGINS_DIR):/app/tests/test_plugins \
	  -v $(CONFIG_PATH):/app/example_config.yaml \
	  -e CONFIG_PATH=example_config.yaml \
	  -e PLUGIN_NAME=$(PLUGIN) \
	  -e PYTHONPATH=/app \
	  $(IMAGE_NAME)

# Clean up cached Python files (local dev)
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -delete

# Build and immediately test plugin
build-and-test: build test-plugin
