import json

import characterProcessing
import config
import languageHandler
from globalPluginHandler import GlobalPlugin

from .interface import add_settings, remove_settings

config.conf.spec["charDescMerge"] = {
    "locales": 'string(default="[]")',
}


class GlobalPlugin(GlobalPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_settings(self.on_save_config)
        self.initial_entries = dict(self.get_description_entries())
        self.merge_descriptions()

    def terminate(self):
        remove_settings()

    def get_description_entries(self, locale=None):
        if locale is None:
            locale = languageHandler.getLanguage()
        return characterProcessing._charDescLocaleDataMap.fetchLocaleData(
            locale
        )._entries

    def on_save_config(self):
        self.merge_descriptions()

    def get_locales(self):
        return json.loads(config.conf["charDescMerge"]["locales"])

    def merge_descriptions(self):
        entries = self.get_description_entries()
        entries.clear()
        entries.update(self.initial_entries)
        for locale in self.get_locales():
            entries.update(self.get_description_entries(locale))
