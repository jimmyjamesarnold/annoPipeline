import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='annoPipeline',
    version='0.0.1',
    author='Jim Arnold',
    author_email='jimmyjamesarnold@gmail.com',
    packages=setuptools.find_packages(),
    url='https://github.com/jimmyjamesarnold/annoPipeline',
    scripts=[],
    description='API-enabled Gene Annotation.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy >= 1.16.2",
        "pandas >= 0.24.2",
        "Biopython >= 1.73",
        "openpyxl >= 2.6.1",
        "requests >= 2.21.0",
    ],
)