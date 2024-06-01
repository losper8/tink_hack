import json
import uuid

with open('../data/norm_dataset_clean.json', 'r') as f:
    data = json.load(f)

for item in data:
    # add id as uuid
    item['id'] = str(uuid.uuid4())

with open('../data/norm_dataset_clean_with_uuid.json', 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
