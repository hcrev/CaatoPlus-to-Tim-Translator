import sys
import datetime
import hashlib
import csv
import json

class Main:

    def __init__(self):

        self.extract_caato_data(sys.argv[1])

        self.generate_tim_data()

        self.json_dump()

    def generate_hash(self, str):
        return hashlib.sha1(str.encode()).hexdigest()

    def convert_date(self, date):
        return datetime.datetime.strptime(date, '%m/%d/%y, %H:%M').timestamp()*1000

    def get_now_time(self):
        return datetime.datetime.now().timestamp()*1000

    def extract_caato_data(self, caato_file):

        self.credit = "Time tracked with Caato Time Tracker+ for Mac"

        reader = csv.DictReader(open(caato_file, 'r'))
        # Iterate over the rows and map values to a list of dictionaries containing key/value pairs
        self.caato_dict = [line for line in reader if not (line["FOLDER"] == self.credit)]

        return self.caato_dict


    def generate_tim_data(self):

        self.tim_dict = {
            "tasks": {},
            "groups": {},
            "nodes": []
        }

        self.nodes = {}

        for i, item in enumerate(self.caato_dict):

            self.activity_hash = self.generate_hash(item["PROJECT"] + item["ACTIVITY"])
            self.project_hash = self.generate_hash(item["PROJECT"])

            self.item = item

            self.generate_tim_tasks()
            self.generate_tim_records()
            self.generate_tim_groups()

            self.nodes[self.activity_hash] = {"id": self.activity_hash, "parent": self.project_hash}
            self.nodes[self.project_hash] = {"id": self.project_hash}

        self.generate_tim_nodes()

        return self.tim_dict

    def generate_tim_tasks(self):
        self.tim_dict["tasks"].setdefault(self.activity_hash, {
            "records": [],
            "id": self.activity_hash,
            "title": self.item["ACTIVITY"],
            "createdAt": self.get_now_time(),
            "updatedAt": self.get_now_time()
        })

    def generate_tim_records(self):
        self.tim_dict["tasks"][self.activity_hash]["records"].append({
            "start": self.convert_date(self.item["START"]),
            "end": self.convert_date(self.item["END"]),
            "note": self.item["NOTES"]
        })

    def generate_tim_groups(self):
        self.tim_dict["groups"].setdefault(self.project_hash, {
            "id": self.project_hash,
            "title": self.item["PROJECT"],
            "createdAt": self.get_now_time(),
            "updatedAt": self.get_now_time()
        })

    def generate_tim_nodes(self):
        self.tim_dict["nodes"] = list(set(self.tim_dict["nodes"]))
        for key, node in self.nodes.items():
            self.tim_dict["nodes"].append(node)

    def json_dump(self):
        print(json.dumps(self.tim_dict))



if __name__ == "__main__":
    Main()
