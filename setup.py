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
    python_requires=">=3.7",
    install_requires=[
        "cx-Oracle==8.1.0",
        "Flask==1.1.2",
        "flask-restx==0.2.0",
        "flask_accepts==0.17.4",
        'boto3==1.12.36',
        'botocore==1.15.36',
        'PyYAML==5.3.1',
        'pyconfig @ https://github.com/huit/pyconfig/archive/v0.0.1.tar.gz#egg=pyconfig'
        'pyslack @ https://github.com/huit/pyslack/archive/v1.0.3.tar.gz#egg=pyslack'
    ]
)