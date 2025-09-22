import re

name_pattern = re.compile(r"^([a-z]+)([-']?)([a-z]+)$",re.IGNORECASE)
string_pattern = re.compile(r"[a-z]+", re.IGNORECASE)