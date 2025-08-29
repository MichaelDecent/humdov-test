# Simple Makefile to manage Docker image lifecycle

# Variables (override on the command line: make build TAG=v1)
REGISTRY ?=
DOCKER_USER ?=
IMAGE_NAME ?= humdov-api
TAG ?= latest
PORT ?= 8000
VOLUME ?= homdov_app_data

# Derived image references
IMAGE_REPO := $(if $(DOCKER_USER),$(DOCKER_USER)/$(IMAGE_NAME),$(IMAGE_NAME))
IMAGE_BASE := $(if $(REGISTRY),$(REGISTRY)/$(IMAGE_REPO),$(IMAGE_REPO))
IMAGE := $(IMAGE_BASE):$(TAG)

.PHONY: help build run compose-up compose-down logs tag push publish login clean

help:
	@echo "Targets:"
	@echo "  build        Build Docker image (TAG=$(TAG))"
	@echo "  run          Run container on port $(PORT) with volume $(VOLUME)"
	@echo "  compose-up   Run via docker compose (detached)"
	@echo "  compose-down Stop compose stack"
	@echo "  logs         Tail compose logs"
	@echo "  tag          Retag an existing image (FROM_TAG, TAG)"
	@echo "  push|publish Push image to registry (REGISTRY/DOCKER_USER configurable)"
	@echo "  login        docker login to REGISTRY (default Docker Hub if empty)"
	@echo "  clean        Remove local image"
	@echo ""
	@echo "Examples:" 
	@echo "  make build TAG=v1"
	@echo "  make push DOCKER_USER=myuser TAG=v1"
	@echo "  make push REGISTRY=ghcr.io DOCKER_USER=myorg TAG=v1"

build:
	docker build -t $(IMAGE) .

run:
	@docker volume create $(VOLUME) >/dev/null
	docker run --rm -p $(PORT):8000 \
	  -e DATABASE_URL=sqlite:////data/app.db \
	  -v $(VOLUME):/data \
	  $(IMAGE)

compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

logs:
	docker compose logs -f

# Retag an image built as :FROM_TAG to :TAG
FROM_TAG ?= latest
tag:
	docker tag $(IMAGE_BASE):$(FROM_TAG) $(IMAGE)

push publish:
	@echo "Pushing $(IMAGE)"
	docker push $(IMAGE)

login:
	@echo "Logging in to registry: '$(if $(REGISTRY),$(REGISTRY),docker.io)'"
	docker login $(REGISTRY)

clean:
	-docker rmi $(IMAGE) || true

