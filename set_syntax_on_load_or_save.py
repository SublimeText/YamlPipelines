import sublime
import sublime_plugin
from pathlib import Path


class YamlFileOpenedEventListener(sublime_plugin.ViewEventListener):
    @classmethod
    def is_applicable(cls, settings):
        return settings.get('syntax', '') == 'Packages/YAML/YAML.sublime-syntax'

    def on_load_async(self):
        self.set_syntax_if_filepath_applicable()

    def on_save_async(self):
        self.set_syntax_if_filepath_applicable()

    def set_syntax_if_filepath_applicable(self):
        if filename := self.view.file_name():
            if Path(filename).match('**/.github/workflows/**'):
                self.view.assign_syntax('scope:source.yaml.pipeline.github-actions')
