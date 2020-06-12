import json

def extract_start_end(file_name):
    with open(file_name) as json_file:
        body = json.load(json_file)
        print(body['messages'].keys())

        keys = list(body['messages'].keys())
        start = keys[0]
        end = keys[-1]

        return (body['messages'][start][0], body['messages'][end][0])

def decorate_start_end(file_name, start_end):
    with open(file_name, 'r') as file1:
        body = json.load(file1)
        log_info = {
            "start_time": start_end[0],
            "end_time": start_end[1]
        }
        body["data"]["log_info"] = log_info
        return body


start_end = extract_start_end('output/0-frame.json')
body = decorate_start_end('output/1-frame-nutonomoy.json', start_end)
with open('output/1-frame-nutonomoy.json', 'w') as outfile:
    json.dump(body, outfile)
