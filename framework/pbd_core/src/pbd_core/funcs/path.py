import os
import tomllib

def find_project_root(start_path="."):
    current = os.path.abspath(start_path)
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, "pyproject.toml")):
            return current
        current = os.path.dirname(current)
    raise FileNotFoundError("No pyproject.toml found")

def detect_source_dirs():
    root = find_project_root()
    pyproject_path = os.path.join(root, "pyproject.toml")

    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    source_dirs = set()

    # Case 1: Hatch + [tool.hatch.build.include]
    try:
        includes = config["tool"]["hatch"]["build"]["include"]
        for path in includes:
            # Only keep directories or valid .py files under src/
            if path.startswith("src/") and (path.endswith(".py") or os.path.isdir(os.path.join(root, path))):
                # extract base source dir (e.g., "src/backend")
                base = path.split("/")[1]  # "backend"
                source_dirs.add(os.path.join(root, "src", base))
    except KeyError:
        pass  # fallback to other methods if needed

    # fallback: search for `src/*/__init__.py`
    if not source_dirs:
        src_path = os.path.join(root, "src")
        if os.path.exists(src_path):
            for name in os.listdir(src_path):
                candidate = os.path.join(src_path, name)
                if os.path.isdir(candidate) and "__init__.py" in os.listdir(candidate):
                    source_dirs.add(candidate)

    return list(source_dirs)


def norm_path(path):
    """将路径转换为标准格式（跨平台兼容）"""
    return os.path.normpath(os.path.abspath(path))