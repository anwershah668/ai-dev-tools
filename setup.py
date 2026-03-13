from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-dev-tools",
    version="0.1.0",
    author="Anwer Shah",
    author_email="anwershah6969@gmail.com",
    description="Open-source tools for automating developer workflows and productivity using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anwershah668/ai-dev-tools",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-dev-tools=ai_dev_tools.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
