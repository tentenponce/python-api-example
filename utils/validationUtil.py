import json

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
		
		if not isinstance(json_object, dict) and not isinstance(json_object, list):
			return False
	except ValueError:
		return False
		
	return True