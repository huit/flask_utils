import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="adex-flask-utils",
    version="0.0.1",
    author="Michael Kerry",
    author_email="michael_kerry@harvard.edu",
    description="A utility for handling config, logging, security and Oracle db operations within a Flask application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.huit.harvard.edu/HUIT/flask_db_util",
    project_urls={
        "Bug Tracker": "https://github.huit.harvard.edu/HUIT/flask_db_util/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "cx-Oracle",
        "Flask",
        "flask-restx",
        "flask_accepts",
        'boto3==1.12.36',
        'botocore==1.15.36',
        'PyYAML==5.3.1',
        'requests==2.25.1'
    ]
)