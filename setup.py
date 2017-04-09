from setuptools import setup

setup(
    name="systemMonitor",
    version="0.0.1",
    author="Serhat Murat Pala",
    author_email="pala@linux.com",
    description="An application to monitor the use of system resources and ddos detecter",
    license="MIT",
    packages=['Monitor'],
    requires=["psutil","termcolor"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'systemMonitor = Monitor.__main__',
        ]
    }
)
