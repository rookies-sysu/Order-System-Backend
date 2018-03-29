deploy:
	docker build -t tiny-hippo:latest .
	docker run -d -p 5000:5000  --name=hippo tiny-hippo 