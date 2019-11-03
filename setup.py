from setuptools import setup

readme = ""
with open("README.md") as f:
    readme = f.read()

setup(
    name="gitrange",
    version="v0.0.4",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Craig Weber",
    author_email="weberc2@gmail.com",
    url="https://github.com/weberc2/gitrange",
    py_modules=["gr"],
    entry_points={"console_scripts": ["gr = gr:main"]},
    project_urls={
        "Documentation": "https://github.com/weberc2/gitrange/README.md",
        "Source": "https://github.com/weberc2/gitrange",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
