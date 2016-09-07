import json

class ModelData:

    config_path = "./config/config.json"

    def __init__(self):
        self.config = self.load_config(ModelData.config_path)
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

    def load_config(self, config_file):
        config = {}
        with open(config_file, 'r') as rfile:
            config.update(json.load(rfile))
        return config
