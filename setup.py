from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="readme-generator",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="LLM Agent for automatic README generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/readme-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "readme-generator=src.main:main",
        ],
    },
)
