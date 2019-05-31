from python_wrapper.blacklist_api import Configuration, BlacklistApi

configuration = Configuration(username='messente', password='piret')
blacklit_api = BlacklistApi(configuration)

try:
    status_code, response_json = blacklit_api.add_to_blacklist("87654321")
    print(f"Status code: {status_code}, body: {response_json}")

except Exception as e:
    print("Exception when calling add_to_blacklist: %s\n" % e)

try:
    status_code, response_json = blacklit_api.remove_from_blacklist("87654321")
    print(f"Status code: {status_code}, body: {response_json}")

except Exception as e:
    print("Exception when calling remove_from_blacklist: %s\n" % e)

try:
    status_code, response_json = blacklit_api.fetch_blacklist()
    print(f"Status code: {status_code}, body: {response_json}")

except Exception as e:
    print("Exception when calling fetch_blacklist: %s\n" % e)