import os
import json
from constantes import pwd_dir


def verify_pwd():
    pwd = os.path.join(pwd_dir, 'pwd' + ".json")
    if not os.path.exists(pwd_dir):
        os.makedirs(pwd_dir)
    with open(pwd, "w") as f:
        json.dump(pwd, f, indent=4, ensure_ascii=True)
