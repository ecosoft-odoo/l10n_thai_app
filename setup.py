from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in l10n_thai_app/__init__.py
from l10n_thai_app import __version__ as version

setup(
	name="l10n_thai_app",
	version=version,
	description="Thai Localization",
	author="Ecosoft",
	author_email="kittiu@ecosoft.co.th",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
