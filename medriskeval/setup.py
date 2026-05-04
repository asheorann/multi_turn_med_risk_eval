from setuptools import setup, find_packages

setup(
    name="medriskeval",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "datasets>=2.0.0",
        "pydantic>=2.0.0",
        "typer>=0.9.0",
        "pyyaml>=6.0.0",
        "openai>=1.0.0",
        "httpx>=0.24.0",
        "rich>=13.0.0",
        "tqdm>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "medriskeval=medriskeval.cli.main:main",
        ],
    },
)
