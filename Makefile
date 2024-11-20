.PHONY: docker-build docker-destroy

docker-up:
	docker compose -f ./docker-compose.yml up -d --build

docker-destroy:
	docker compose -f ./docker-compose.yml down
	chmod +x delete_unused_images.sh && ./delete_unused_images.sh && docker volume prune -f