from setuptools import find_packages, setup

install_requires = [
    "wagtail>=6.0",
    "httpx",
    "faker",
    "django-environ",
]

tests_require = [
    "black",
    "coverage",
    "flake8",
    "isort",
    "pytest",
    "pytest-cov",
    "pytest-django",
    "pytest-mock",
    "pytest-xdist",
    "pytest-asyncio",
]

setup(
    name="wagtail-facebook-events",
    version="0.1.0",
    description="A Wagtail module to import Facebook events",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="G.R Erdtsieck",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    url="https://github.com/yourusername/wagtail-facebook-events",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Wagtail :: 5",
        "Framework :: Wagtail :: 6",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
