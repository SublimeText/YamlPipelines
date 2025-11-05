import sublime_plugin
from wcmatch.glob import BRACE
from wcmatch.glob import globmatch
from wcmatch.glob import GLOBSTAR


def syntax_event_listener(syntax, scope_path_patterns):
    """
    Decorator to create a ViewEventListener class that automatically sets syntax
    based on file path patterns.

    Args:
        syntax: The syntax string to match in is_applicable (e.g., 'Packages/YAML/YAML.sublime-syntax')
        scope_path_patterns: Dictionary mapping file path patterns to scope strings
    """
    def decorator(cls):
        class inner(cls):
            SCOPE_PATH_PATTERNS = scope_path_patterns
            _applicable_syntax = syntax

            @classmethod
            def is_applicable(cls, settings):
                return settings.get('syntax', '') == cls._applicable_syntax

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
        inner.__name__ = cls.__name__
        return inner

    return decorator


@syntax_event_listener(
    syntax='Packages/YAML/YAML.sublime-syntax',
    scope_path_patterns={
        # Some CI pipeline scopes can be deduced from their path when given more context
        # than just an extension. This maps a given path pattern to a scope to apply.
        # The first one that matches will be applied (note that dicts are
        # insertion-ordered as of Python 3.7), but in general they should not overlap.
        '**/.github/workflows/**': 'scope:source.yaml.pipeline.github-actions',
        '**/.github/actions/**/*': 'scope:source.yaml.pipeline.github-actions',
        '*.gitlab-ci.yml': 'scope:source.yaml.pipeline.gitlab',
        '**/templates/**/*.{yml,yaml}': 'scope:source.yaml.helm',
    }
)
class YamlFileOpenedEventListener(sublime_plugin.ViewEventListener):
    pass


@syntax_event_listener(
    syntax='Packages/Text/Plain text.tmLanguage',
    scope_path_patterns={
        '**/templates/**/*.tpl': 'scope:source.yaml.helm',
    }
)
class PlaintextFileOpenedEventListener(sublime_plugin.ViewEventListener):
    pass
