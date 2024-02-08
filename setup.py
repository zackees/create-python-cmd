import os
import re

import setuptools

URL = "https://github.com/zackees/create-python-cmd"

HERE = os.path.dirname(os.path.abspath(__file__))



if __name__ == "__main__":
    setuptools.setup(
        maintainer="Zachary Vorhies",
        long_description_content_type="text/markdown",
        url=URL,
        include_package_data=True,
    )
