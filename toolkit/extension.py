import os
import importlib
import pkgutil
from typing import List

from toolkit.paths import TOOLKIT_ROOT


class Extension(object):
    """Base class for extensions.

    Extensions are registered with the ExtensionManager, which is
    responsible for calling the extension's load() and unload()
    methods at the appropriate times.

    """

    name: str = None
    uid: str = None

    @classmethod
    def get_process(cls):
        # extend in subclass
        pass


def get_all_extensions() -> List[Extension]:
    extension_folders = ["extensions", "extensions_built_in"]
    print(f"Scanning for extensions in folders: {extension_folders}")

    # This will hold the classes from all extension modules
    all_extension_classes: List[Extension] = []

    # Iterate over all directories (i.e., packages) in the "extensions" directory
    for sub_dir in extension_folders:
        extensions_dir = os.path.join(TOOLKIT_ROOT, sub_dir)
        print(f"\nScanning directory: {extensions_dir}")

        for _, name, _ in pkgutil.iter_modules([extensions_dir]):
            print(f"  Found module: {name}")
            try:
                # Import the module
                module = importlib.import_module(f"{sub_dir}.{name}")
                print(f"  Successfully imported {name}")

                # Get the value of the AI_TOOLKIT_EXTENSIONS variable
                extensions = getattr(module, "AI_TOOLKIT_EXTENSIONS", None)

                # Check if the value is a list
                if isinstance(extensions, list):
                    print(f"  Found {len(extensions)} extension(s) in {name}")
                    # Iterate over the list and add the classes to the main list
                    for ext in extensions:
                        print(f"    - {ext.name} ({ext.uid})")
                    all_extension_classes.extend(extensions)
                else:
                    print(
                        f"  No extensions found in {name} (AI_TOOLKIT_EXTENSIONS not a list)"
                    )

            except ImportError as e:
                print(f"  ERROR: Failed to import {name}")
                print(f"  Error details: {str(e)}")

    print(f"\nTotal extensions found: {len(all_extension_classes)}")
    return all_extension_classes


def get_all_extensions_process_dict():
    print("\nBuilding extension process dictionary...")
    all_extensions = get_all_extensions()
    process_dict = {}

    for extension in all_extensions:
        print(f"Getting process for {extension.name}")
        try:
            process_dict[extension.uid] = extension.get_process()
            print(f"Successfully loaded process for {extension.name}")
        except Exception as e:
            print(f"ERROR: Failed to get process for {extension.name}")
            print(f"Error details: {str(e)}")

    print(f"Loaded {len(process_dict)} extension processes")
    return process_dict
