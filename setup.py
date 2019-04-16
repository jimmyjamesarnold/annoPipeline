import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='annoPipeline',
    version='0.0.1',
    author='Jim Arnold',
    author_email='jimmyjamesarnold@gmail.com',
    packages=setuptools.find_packages(),
    url='https://github.com/jimmyjamesarnold/annoPipeline',
    description='API-enabled Gene Annotation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator"
    ],
    install_requires=[
        "numpy >= 1.16.2",
        "pandas >= 0.24.2",
        "Biopython >= 1.73",
        "openpyxl >= 2.6.1",
        "requests >= 2.21.0",
    ]
)