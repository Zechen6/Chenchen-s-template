from flask import Flask
from Services.Rules import rules_manager

app = Flask(__name__)

@app.route("/")

def hello():
	return "Hello World"

@app.route("/test")
def test():
	mgr = rules_manager.Manager()
	mgr.load_rules()
	mgr.judgement_rule()
	# print(mgr.rules_list.json)
	return str(mgr.rules_list.json)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9999)
