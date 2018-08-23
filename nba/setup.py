import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nba-stats',
    version='0.1',
    description='Python utility to easily scrape NBA stats',
    license='MIT',
    author='Hamza Qadeer',
    url='https://github.com/hqadeer/nba-stats.git',
    requires={
        "Selenium",
        "beautifulsoup4",
        "lxml",
    }
)
