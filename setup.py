import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="universal_api",
    version="0.0.7",
    author="Volodymyr Vozniak",
    author_email="vozniak.v.z@gmail.com",
    description="Some useful functions to help you working with API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VolodymyrVozniak/universal-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests==2.25.1',
        'json2xml==3.6.0'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)