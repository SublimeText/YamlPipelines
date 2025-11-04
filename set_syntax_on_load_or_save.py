import sublime_plugin
from wcmatch.glob import BRACE
from wcmatch.glob import globmatch
from wcmatch.glob import GLOBSTAR


class YamlFileOpenedEventListener(sublime_plugin.ViewEventListener):
    # Some CI pipeline scopes can be deduced from their path when given more context
    # than just an extension. This maps a given path pattern to a scope to apply.
    # The first one that matches will be applied (note that dicts are
    # insertion-ordered as of Python 3.7), but in general they should not overlap.
    SCOPE_PATH_PATTERNS = {
        '**/.github/workflows/**': 'scope:source.yaml.pipeline.github-actions',
        '**/.github/actions/**/*': 'scope:source.yaml.pipeline.github-actions',
        '*.gitlab-ci.yml': 'scope:source.yaml.pipeline.gitlab',
        '**/templates/**/*.{yml,yaml}': 'scope:source.yaml.helm'
    }

    @classmethod
    def is_applicable(cls, settings):
        return settings.get('syntax', '') == 'Packages/YAML/YAML.sublime-syntax'

    def on_load(self):
        self.set_syntax_if_filepath_applicable()

    def on_save_async(self):
        self.set_syntax_if_filepath_applicable()

    def set_syntax_if_filepath_applicable(self):
        if filename := self.view.file_name():
            for pattern, scope in self.SCOPE_PATH_PATTERNS.items():
                if globmatch(filename, pattern, flags=GLOBSTAR | BRACE):
                    self.view.assign_syntax(scope)
                    break


class PlaintextFileOpenedEventListener(sublime_plugin.ViewEventListener):
    SCOPE_PATH_PATTERNS = {
        '**/templates/**/*.tpl': 'scope:source.yaml.helm'
    }

    @classmethod
    def is_applicable(cls, settings):
        return settings.get('syntax', '') == 'Packages/Text/Plain text.tmLanguage'

    def on_load(self):
        self.set_syntax_if_filepath_applicable()

    def on_save_async(self):
        self.set_syntax_if_filepath_applicable()

    def set_syntax_if_filepath_applicable(self):
        if filename := self.view.file_name():
            for pattern, scope in self.SCOPE_PATH_PATTERNS.items():
                if globmatch(filename, pattern, flags=GLOBSTAR | BRACE):
                    self.view.assign_syntax(scope)
                    break
