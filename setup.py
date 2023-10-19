from setuptools import setup

setup(
    name='csvlineparser',
    version='1.0.0',
    description='csvlineparser',
    url='---',
    author='raoulsson',
    author_email='hello@raoulsson.com',
    license='MIT License',
    packages=['csvlineparser.clientutils', 'csvlineparser.excelexport', 'csvlineparser.core', 'examples'],
    include_package_data=True,
    install_requires=['pandas~=2.1.1', 'openpyxl==3.1.2', 'xlsxwriter==3.1.5'],
    classifiers=[
        'Development Status :: Release v0.1.0',
        'Intended Audience :: Private Client',
        'License :: MIT License',
        'Operating System :: Linux, Windows, Mac OS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.9',
    setup_requires=['setuptools-git-versioning'],
    setuptools_git_versioning={
        "dirty_template": "{tag}",
    }
)
