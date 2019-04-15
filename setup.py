from setuptools import setup

setup(
    name='InterviewTest',
    version='0.1dev',
    author='J. Arnold',
    author_email='jimmyjamesarnold@gmail.com',
    packages=['annoPipeline',],
    url='',
    scripts=[],
    description='API-enabled Gene Annotation.',
    long_description=open('README.txt').read(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    install_requires=[
        "numpy >= 1.16.2",
        "pandas >= 0.24.2",
        "Biopython >= 1.73",
        "openpyxl >= 2.6.1",
        "requests >= 2.21.0",
    ],
)