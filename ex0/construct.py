import sys, os

print("\nMATRIX STATUS: You're still plugged in\n")
if sys.prefix != sys.base_prefix:
    print("Current python:", sys.executable)
    print("Virtual Environment:", os.path.basename(sys.prefix))
    print("Environment path:", sys.prefix)
    print("\nSUCCESS: You're in an isolated environment!\nSafe to install packages without affecting the global system.\n")
    site_packages = os.path.join(sys.prefix, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
    print("Package installation path:\n", site_packages)
else:
    print("Current python:", sys.executable)
    print("Virtual Environment: Not detected\n")
    print("WARNING: You're in the global environment!\nThe machines can see everything you install.")
    print("To enter the construct, run:\npython -m venv matrix_env\nsource matrix_env/bin/activate # On Unix\nmatrix_env\\Scripts\\activate # On Windows\n")
    print("Then run this program again")

