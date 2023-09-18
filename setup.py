import setuptools, glob
from pathlib import Path

#note: build this package with the following command:
#pip wheel --no-deps -w dist .

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text()

setuptools.setup(
  name="freedns-client",
  version="0.1.0",
  author="ading2210",
  license="GPLv3",
  description="A Python package for interacting with FreeDNS.afraid.org",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=["freedns"],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent"
  ],
  python_requires=">=3.7",
  package_dir={
    "": "src"
  },
  package_data={},
  include_package_data=True,
  install_requires=[
    "lxml",
    "cssselect",
    "requests",
  ],
  url="https://github.com/ading2210/freedns-client"
)