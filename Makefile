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

dbtest:
	# Test db operator locally
	# wait mysql db can connect
	while ! nc -z 127.0.0.1 3306; do sleep 3; done

	# prepare for unit tests
	cp -r ./app/dbTools ./tests
	cp ./tests/dbConfig_TEST.py ./tests/dbTools/dbConfig.py

	# Run the tests
	cd tests && python test_suite.py
	
	# remove the temp file
	rm -rf ./tests/dbTools