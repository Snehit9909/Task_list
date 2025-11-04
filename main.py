import importlib
import os

def load_plugins(folder="plugins"):
    """Load all plugin modules that define a run(data) function."""
    plugins = []
    for file in os.listdir(folder):
        if file.endswith(".py"):
            name = file[:-3]
            module = importlib.import_module(f"{folder}.{name}")
            if hasattr(module, "run"):
                plugins.append(module.run)
    return plugins

def main():
    data = "Welcome to India"
    print("Original:", data)

    # Load and apply plugins in sequence
    for plugin in load_plugins():
        data = plugin(data)

    print("Final:", data)

if __name__ == "__main__":
    main()
