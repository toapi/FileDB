import ast
import re

from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('FileDB/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='FileDB',
    version=version,
    description='provide local file store.',
    author='qiang wu',
    author_email='wuqiangroy@gmail.com',
    url='https://github.com/wuqiangroy/FileDB',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "sqlalchemy",
        "click"
    ],
    license='Apache 2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'FileDB=FileDB.cli:cli',
        ],
    },
    py_modules=['FileDB'],
    include_package_data=True,
    zip_safe=False
)