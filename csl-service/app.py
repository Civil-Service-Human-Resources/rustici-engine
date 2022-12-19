from flask import Flask, request
import json

app = Flask(__name__)

@app.post("/")
def hello_world():
	app.logger.info("Request received")
	data = request.json
	if (data):
		app.logger.info(f"Completion status (registrationCompletion): {data['registrationCompletion']}")
		app.logger.info(f"Last updated (updated): {data['updated']}")
		app.logger.info(f"Created (createdDate): {data['createdDate']}")
		app.logger.info(f"Registration ID AKA module record UID (id): {data['id']}")
		with open("req.json", "a") as file:
			app.logger.info("Writing")
			file.write(f"{json.dumps(data)}\n\n")
	return "OK"

if __name__ == '__main__':
  app.run(port=9003, host='0.0.0.0', debug=True)