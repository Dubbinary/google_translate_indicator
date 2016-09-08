import json

class ModelData:

    config_path = "./config/config.json"

    def __init__(self):
        self.config = self.load_config()
        self.lang_from = self.config["lang_from"]
        self.lang_to = self.config["lang_to"]
        self.languages = self.config["languages"]

    def get_lang_from(self):
        return self.lang_from

    def set_lang_from(self, new_from):
        self.lang_from = new_from

    def get_lang_to(self):
        return self.lang_to

    def set_lang_to(self, new_to):
        self.lang_to = new_to

    def get_languages(self):
        return self.languages

    def load_config(self):
        config = {}
        with open(ModelData.config_path, 'r') as rfile:
            config.update(json.load(rfile))
        return config

    def update_config(self):
        self.config["lang_from"] = self.lang_from
        self.config["lang_to"] = self.lang_to
        with open(ModelData.config_path, 'w') as wfile:
            json.dump(self.config, wfile)
