from setuptools import setup, find_packages

setup(
    name='job_shop',
    version='1.0',
    url='https://github.com/DrCapa/job_shop',
    author='Rico Hoffmann',
    author_email='rico.hoffmann@libero.it',
    description='README',
    packages=find_packages(),
    install_requires=['pandas >= 0.23.4', 'pyomo >= 5.5.0',
                      'numpy >= 1.15.2', 'matplotlib >= 3.0.2',
                      'xlsxwriter >= 1.0.7', 'plotly >= 3.7.1']
)
