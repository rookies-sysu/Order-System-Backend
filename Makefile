deploy:
	docker-compose up -d
	sleep 60
	curl localhost:8080/api/insert_fake_data2

rebuild:
	docker-compose down
	docker-compose build web db nginx
	docker-compose up -d

redeploy:
	docker-compose down
	sudo rm -rf /opt/mysql_data
	docker-compose build web db nginx
	docker-compose up -d
	sleep 60
	curl localhost:8080/api/insert_fake_data2

dbtest:
	# rebuild TINYHIPPOTEST database for unittest
	make redeploy
	# wait mysql db can connect
	while ! nc -z 127.0.0.1 3306; do sleep 3; done

	cp -r ./app/dbTools ./tests
	cp ./tests/dbConfig_TEST.py ./tests/dbTools/dbConfig.py

	# Run the tests
	cd tests && python3 test_suite.py
	
	# remove the temp file
	rm -rf ./tests/dbTools

	# DB TEST Finished! Please check the test result in UnittestTextReport.txt!