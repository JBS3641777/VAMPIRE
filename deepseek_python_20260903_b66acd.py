from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="k2-driver",
    version="3.0.0",
    author="TeddyBear Financial Systems",
    author_email="support@teddybear-financial.com",
    description="K2 Driver - High-Output Circuit Financial Transaction Processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teddybear-financial/k2-driver",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
        "cryptography>=38.0.0",
        "pandas>=1.5.0",
        "numpy>=1.23.0",
    ],
    entry_points={
        "console_scripts": [
            "k2-driver=k2_driver.cli:main",
        ],
    },
)