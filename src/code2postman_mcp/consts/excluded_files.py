"""
This module contains dictionaries of regex patterns for files and directories
that should be excluded from tree directory listing for various programming languages.
"""

# Languages that are supported for filtering
from enum import Enum

class Language(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    GOLANG = "go"
    RUBY = "ruby"
    RUST = "rust"
    CSHARP = "csharp"
    GENERIC = "generic"

EXCLUDED_ITEMS = {
    Language.PYTHON: {
        "directories": [
            r"^\.venv$",
            r"^venv$",
            r"^__pycache__$",
            r"^\.pytest_cache$",
            r"^\.mypy_cache$",
            r"^\.coverage$",
            r"^build$",
            r"^dist$",
            r"^.*\.egg-info$",
            r"^\.ipynb_checkpoints$",
            r"^\.git$",
            r"^\.github$",
        ],
        "files": [
            r"^__init__\.py$",
            r"^.*\.pyc$",
            r"^.*\.pyo$",
            r"^.*\.pyd$",
            r"^\.coverage$",
            r"^\.DS_Store$",
            r"^.*\.egg-info$",
        ],
    },
    Language.JAVASCRIPT: {
        "directories": [
            r"^node_modules$",
            r"^bower_components$",
            r"^dist$",
            r"^build$",
            r"^coverage$",
            r"^\.next$",
            r"^\.nuxt$",
            r"^\.git$",
            r"^\.github$",
        ],
        "files": [
            r"^package-lock\.json$",
            r"^yarn\.lock$",
            r"^\.DS_Store$",
            r"^\.env$",
            r"^\.env\.local$",
            r"^.*\.log$",
        ],
    },
    Language.JAVA: {
        "directories": [
            r"^target$",
            r"^build$",
            r"^out$",
            r"^\.gradle$",
            r"^\.idea$",
            r"^bin$",
            r"^\.git$",
            r"^\.github$",
        ],
        "files": [
            r"^.*\.class$",
            r"^.*\.jar$",
            r"^.*\.war$",
            r"^\.DS_Store$",
            r"^.*\.log$",
        ],
    },
    Language.GOLANG: {
        "directories": [
            r"^vendor$",
            r"^bin$",
            r"^dist$",
            r"^\.git$",
            r"^\.github$",
        ],
        "files": [
            r"^go\.sum$",
            r"^\.DS_Store$",
        ],
    },
    Language.RUBY: {
        "directories": [
            r"^vendor$",
            r"^\.bundle$",
            r"^coverage$",
            r"^tmp$",
            r"^log$",
            r"^\.git$",
            r"^\.github$",
        ],
        "files": [
            r"^.*\.gem$",
            r"^Gemfile\.lock$",
            r"^\.DS_Store$",
            r"^.*\.log$",
        ],
    },
    Language.RUST: {
        "directories": [
            r"^target$",
            r"^\.cargo$",
            r"^\.git$",
            r"^\.github$",
        ],
        "files": [
            r"^Cargo\.lock$",
            r"^\.DS_Store$",
        ],
    },
    Language.CSHARP: {
        "directories": [
            r"^bin$",
            r"^obj$",
            r"^packages$",
            r"^\.vs$",
            r"^\.vscode$",
            r"^\.git$",
            r"^\.github$",
        ],
        "files": [
            r"^.*\.dll$",
            r"^.*\.exe$",
            r"^.*\.pdb$",
            r"^\.DS_Store$",
        ],
    },
    Language.GENERIC: {
        "directories": [
            r"^\.git$",
            r"^\.github$",
            r"^\.svn$",
            r"^\.hg$",
            r"^\.idea$",
            r"^\.vscode$",
            r"^node_modules$",
            r"^dist$",
            r"^build$",
            r"^bin$",
            r"^obj$",
            r"^out$",
            r"^target$",
            r"^vendor$",
            r"^coverage$",
            r"^logs$",
            r"^temp$",
            r"^tmp$",
        ],
        "files": [
            r"^\.DS_Store$",
            r"^.*\.log$",
            r"^.*\.tmp$",
            r"^.*\.bak$",
            r"^.*\.swp$",
            r"^.*\.cache$",
            r"^\.env$",
            r"^.*\.lock$",
            r"^.*\.tgz$",
            r"^.*\.zip$",
            r"^.*\.tar\.gz$",
        ],
    },
} 