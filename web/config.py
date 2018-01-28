import json
import os
with open(os.path.join(os.path.abspath('.'), 'secrets.json')) as f:
    secrets = json.load(f)
