import sys

import addonHandler
import config
import gui
import languageHandler
import wx
from gui.nvdaControls import CustomCheckListBox

from .interface_helpers import ConfigBoundSettingsPanel, bind_with_config

addonHandler.initTranslation()


class CharDescMergeSettingsPanel(ConfigBoundSettingsPanel):
    title = addonHandler.getCodeAddon().manifest["summary"]

    def makeSettings(self, settings_sizer):
        self.config = config.conf["charDescMerge"]
        sizer = gui.guiHelper.BoxSizerHelper(self, sizer=settings_sizer)
        # bind_with_config will try to check checkboxes, so let's add elements first
        locales_list = sizer.addLabeledControl(
            _("Locales to merge descriptions"),
            CustomCheckListBox,
        )
        for code, name in languageHandler.getAvailableLanguages(True):
            locales_list.Append(name, code)
        self.locales_list = bind_with_config(locales_list, "locales")
        self.locales_list.SetSelection(0)


def add_settings(on_save_callback):
    CharDescMergeSettingsPanel.on_save_callback = on_save_callback
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
        CharDescMergeSettingsPanel
    )


def remove_settings():
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
        CharDescMergeSettingsPanel
    )
