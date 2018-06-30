deploy:
	docker-compose up -d

rebuild:
	docker-compose down
	docker-compose build web db nginx
	docker-compose up -d

redeploy:
	docker-compose down
	sudo rm -rf /opt/mysql_data
	docker-compose build web db nginx
	docker-compose up -d