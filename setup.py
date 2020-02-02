import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="helios",  # Replace with your own username
    version="0.0.1",
    author="Rurushu0",
    author_email="rurushu0.zen@gmail.com",
    description="A Python package for manipulating source files, projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="<https://github.com/rurushu0/helios" >,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
