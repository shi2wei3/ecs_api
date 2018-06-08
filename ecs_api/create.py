from ecs_api import ECSApi
import json
import sys

json_spec = {
    "server": {
        "availability_zone": "cn-east-2a",
        "name": "ecs-wshi-api",
        "imageRef": "726802ee-a5c6-4b2e-9a2f-66f24f205313",
        "root_volume": {
            "volumetype": "SATA",
            "size": 40
        },
        "flavorRef": "s1.medium",
        "vpcid": "3a4250b1-9256-4b04-8607-dd220c6ae991",
        "security_groups": [
            {
                "id": "088dcd24-3a1d-45b2-bafe-370eec5dffab"
            }
        ],
        "nics": [
            {
                "subnet_id": "960f27f3-37b3-4a39-8746-2746acb991a2"
            }
        ],
        "publicip": {
            "eip": {
                "iptype": "5_sbgp",
                "bandwidth": {
                    "size": 1,
                    "sharetype": "PER"
                }
            }
        },
        "key_name": "wshi",
        "count": 1
    }
}


def ecs_create(json_ecs):
    j_content = ECSApi().create_ecss(json_ecs)
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def help():
    return "spec\t\t\tCreate a example config file\n<ConfigFile>\t\tCreate a instance based on <ConfigFile>"


def main(argv=sys.argv):
    if len(argv) != 2:
        print("Error: ecs create requires 1 argument")
    if argv[1] == 'spec':
        with open('ecs_json', 'w') as fp:
            json.dump(json_spec, fp, indent=4)
    else:
        with open(argv[1], 'r') as fp:
            json_ecs = json.load(fp)
        ecs_create(json_ecs)


if __name__ == '__main__':
    main()
