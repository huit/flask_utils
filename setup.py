import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aais-flask-db-util",
    version="0.0.1",
    author="Jinesh Mehta",
    author_email="jinesh_mehta@harvard.edu",
    description="A utility for handling Oracle db operations within a Flask application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.huit.harvard.edu/HUIT/flask_db_util",
    project_urls={
        "Bug Tracker" : "https://github.huit.harvard.edu/HUIT/flask_db_util/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)