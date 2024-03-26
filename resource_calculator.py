import configs_manager
import sys


class ResourceCalculator:
    def __init__(self, json_path):
        resources_data = configs_manager.Config(json_path, {})

        self.resources = configs_manager.ConfigManager(resources=resources_data)
        self.resources.update_configs()
    def get_component_by_name(self, name:str):
        for i in self.resources.get_config("resources", False).keys():
            if name.lower() in map(lambda x: x.lower(), self.resources.get_config(f"resources.{i}.names", False)):
                return i
        
        print("No such resource: {}".format(name))
        return None
    def is_primary(self, id):
        return self.resources.get_config(f"resources.{id}.primary", False)
    def get_craft_components(self, id):
        if not self.is_primary(id):
            return self.resources.get_config(f"resources.{id}.craft", False)
        else:
            print("Resource {} is primary".format(id))
    def get_component_name_by_id(self, id, name_number=0):
        return self.resources.get_config(f"resources.{id}.names.{name_number}", False)
    def get_all_component_names(self, id):
        return self.resources.get_config(f"resources.{id}.names", False)
    def get_all_components_ids(self):
        return self.resources.get_config("resources", False).keys()