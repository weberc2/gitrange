from setuptools import setup

setup(
    name="gitrange",
    py_modules=["gr"],
    entry_points={"console_scripts": ["gr = gr:main"]},
)
