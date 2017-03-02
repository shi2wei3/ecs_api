from ecs_api import ECSApi
import json
import sys

json_spec = {
    "server": {
        "availability_zone": "eu-de-01",
        "name": "ecs-wshi-api",
        "imageRef": "32fda0a4-ab10-4dd4-b398-583a5919cdef",
        "root_volume": {
            "volumetype": "SATA",
            "size": 10
        },  
        "data_volumes": [
            {   
                "volumetype": "SATA",
                "size": 100 
            },  
            {   
                "volumetype": "SSD",
                "size": 100 
            }   
        ],  
        "flavorRef": "normal1",
        "vpcid": "623adb0a-9e35-4611-8c90-6c90d93331d5",
        "security_groups": [
            {   
                "id": "eeebcb30-ad60-4f7f-9be5-0d946cd56fb2"
            }   
        ],  
        "nics": [
            {   
                "subnet_id": "1bff2730-36d5-437b-8e8d-26d388f67eb0"
            }   
        ],  
        "publicip": {
            "id": "948cc53c-469c-412c-81d5-6092107e0e52"
        },  
        "key_name": "KeyPair-wshi",
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
        print("Error: ecs create requires 1 arguement")
    if argv[1] == 'spec':
        with open('ecs_json', 'w') as fp:
            json.dump(json_spec, fp, indent=4)
    else:
        with open(argv[1], 'r') as fp:
            json_ecs = json.load(fp)
        ecs_create(json_ecs)


if __name__ == '__main__':
    main()
