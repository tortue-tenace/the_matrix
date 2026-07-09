from __future__ import annotations

import importlib
import sys
from types import ModuleType
from typing import Any

REQUIRED_PACKAGES: dict[str, str] = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
}
OPTIONAL_PACKAGES: dict[str, str] = {
    "requests": "Network access",
}

DATA_SIZE = 1000
OUTPUT_PATH = "matrix_analysis.png"


def load_module(name: str) -> ModuleType | None:
    try:
        return importlib.import_module(name)
    except ImportError:
        return None


def check_dependencies(
    packages: dict[str, str],
) -> dict[str, ModuleType | None]:
    modules: dict[str, ModuleType | None] = {}
    for name, purpose in packages.items():
        module = load_module(name)
        modules[name] = module
        if module is not None:
            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {name} ({version}) - {purpose} ready")
        else:
            print(f"[MISSING] {name} - {purpose} unavailable")
    return modules


def print_install_instructions(missing: list[str]) -> None:
    names = " ".join(missing)
    print("\nWARNING: Missing dependencies detected!")
    print("\nInstall with pip:")
    print("  pip install -r requirements.txt")
    print(f"  # or individually: pip install {names}")
    print("\nInstall with Poetry:")
    print("  poetry install")
    print(f"  # or individually: poetry add {names}")


def compare_pip_poetry(modules: dict[str, ModuleType | None]) -> None:
    print("\nInstalled package versions:")
    for name, module in modules.items():
        version = (
            getattr(module, "__version__", "unknown")
            if module is not None
            else "not installed"
        )
        print(f"  {name}: {version}")

    print("\npip vs Poetry:")
    print("  pip    - installs from requirements.txt into the active")
    print("           environment, no lock file, versions loosely pinned")
    print("  Poetry - installs from pyproject.toml, resolves the full")
    print("           dependency graph and writes poetry.lock so every")
    print("           install is reproducible")

    prefix = sys.prefix
    if "pypoetry" in prefix:
        print("\nDetected environment: Poetry-managed virtual environment")
    elif sys.prefix != sys.base_prefix:
        print("\nDetected environment: pip/venv-managed virtual environment")
    else:
        print("\nDetected environment: global Python (no virtual env)")


def fetch_matrix_data_from_api(requests_module: ModuleType) -> list[float]:
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests_module.get(url, timeout=5)
    response.raise_for_status()
    payload = response.json()
    return [float(len(str(item))) for item in payload[:DATA_SIZE]]


def generate_matrix_data(numpy_module: ModuleType, size: int) -> Any:
    generator = numpy_module.random.default_rng(42)
    return generator.normal(loc=0.0, scale=1.0, size=size)


def analyze_matrix_data(pandas_module: ModuleType, data: Any) -> Any:
    frame = pandas_module.DataFrame({"signal": data})
    frame["cumulative"] = frame["signal"].cumsum()
    return frame


def visualize(pyplot_module: ModuleType, frame: Any, path: str) -> None:
    figure, axis = pyplot_module.subplots()
    axis.plot(frame["cumulative"])
    axis.set_title("Matrix Data Analysis")
    axis.set_xlabel("Data point")
    axis.set_ylabel("Cumulative signal")
    figure.savefig(path)
    pyplot_module.close(figure)


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")

    use_api = "--api" in sys.argv
    packages = dict(REQUIRED_PACKAGES)
    if use_api:
        packages.update(OPTIONAL_PACKAGES)

    print("Checking dependencies:")
    modules = check_dependencies(packages)
    missing = [name for name, module in modules.items() if module is None]

    required_missing = [
        name for name in REQUIRED_PACKAGES if modules.get(name) is None
    ]
    if required_missing:
        print_install_instructions(missing)
        compare_pip_poetry(modules)
        return

    numpy_module = modules["numpy"]
    pandas_module = modules["pandas"]
    matplotlib_module = modules["matplotlib"]
    assert numpy_module is not None
    assert pandas_module is not None
    assert matplotlib_module is not None
    pyplot_module = importlib.import_module("matplotlib.pyplot")

    print("\nAnalyzing Matrix data...")
    data: Any = None
    requests_module = modules.get("requests")
    if use_api and requests_module is not None:
        try:
            data = fetch_matrix_data_from_api(requests_module)
            print(f"Fetched {len(data)} data points from the API...")
        except Exception as error:
            print(f"API fetch failed ({error}), falling back to numpy...")

    if data is None:
        print(f"Processing {DATA_SIZE} data points...")
        data = generate_matrix_data(numpy_module, DATA_SIZE)

    frame = analyze_matrix_data(pandas_module, data)

    print("Generating visualization...")
    visualize(pyplot_module, frame, OUTPUT_PATH)

    print("\nAnalysis complete!")
    print(f"Results saved to:  {OUTPUT_PATH}")

    compare_pip_poetry(modules)


if __name__ == "__main__":
    main()
