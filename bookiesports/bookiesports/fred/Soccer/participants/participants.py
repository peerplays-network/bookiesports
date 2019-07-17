import yaml

for f in [
    "EPL_Teams_2017-18.yaml",
    "SLL_Teams_2017-18.yaml"
]:
    with open(f, "r") as fid:
        d = yaml.load(fid)
    for p in d["participants"]:
        name = p["name"]
        p["name"] = {"en": name}
    with open(f, "w") as fid:
        dump = yaml.dump(d, default_flow_style=False)
        fid.write(dump)
        print(dump)
