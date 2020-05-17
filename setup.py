import pathlib
from setuptools import setup

README_PATH = pathlib.Path(__file__).parent / 'README.md'
README_TEXT = README_PATH.read_text()

setup(
    name='htmlcreator',
    version='0.4.0',
    license='MIT',
    description='Build standalone HTML documents using Python code',
    long_description=README_TEXT,
    long_description_content_type='text/markdown',
    author='Arkadiusz Nowaczyński',
    author_email='ar.nowaczynski@gmail.com',
    url='https://github.com/ar-nowaczynski/htmlcreator',
    packages=['htmlcreator'],
    package_data={
        'htmlcreator': ['*.css'],
    },
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.14.0',
        'pandas>=0.22.0',
        'Pillow>=5.0.0',
        'plotly>=4.6.0',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
