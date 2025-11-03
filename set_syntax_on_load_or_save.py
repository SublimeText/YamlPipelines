import sublime
import sublime_plugin
from pathlib import Path

# Some CI pipeline scopes can be deduced from their path when given more context
# than just an extension. This maps a given path pattern to a scope to apply.
# The first one that matches will be applied (note that dicts are
# insertion-ordered as of Python 3.7), but in general they should not overlap.
SCOPE_PATH_PATTERNS = {
    '**/.github/workflows/**': 'scope:source.yaml.pipeline.github-actions',
    '**/.github/actions/**/*': 'scope:source.yaml.pipeline.github-actions',
    '*.gitlab-ci.yml': 'scope:source.yaml.pipeline.gitlab',
    '*/templates/**/*': 'scope:source.yaml.go',
    '*/templates/*': 'scope:source.yaml.go',
}


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
            for pattern, scope in SCOPE_PATH_PATTERNS.items():
                if Path(filename).match(pattern):
                    self.view.assign_syntax(scope)
                    break
