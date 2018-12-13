from setuptools import setup, find_packages

setup(
    name='tdtgtd',
    version="0.1",
    packages=["tdtgtd"],
    # url='https://github.com/Tinche/aiofiles',
    license="GPL 2.0",
    author="David Steele",
    author_email='dsteele@gmail.com',
    description="Todo.txt support scripts for GTD.",
    long_description="no",
    entry_points={
        "console_scripts": [
            "tdtcleanup = tdtgtd.tdtcleanup:cleanup",
            "tdtbackup = tdtgtd.tdtbackup:backup",
            "tdtlist = tdtgtd.tdtlist:list_tasks",
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
