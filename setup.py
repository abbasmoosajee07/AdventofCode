from setuptools import setup, find_packages

setup(
    name="MainRepo",  # Name of your package
    version="0.1",
    packages=find_packages(),  # Automatically find all packages (e.g., Benchmark)
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    install_requires=[],  # Add dependencies if your repo requires any (e.g., pandas, matplotlib)
)
