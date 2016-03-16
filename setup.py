from setuptools import setup

setup(
    name="django-babik-card-primitives",
    version="0.1.0",
    description="Basic functionallity for handling credit card information",
    author="Aubrey Stark-Toller",
    author_email="aubrey@deepearth.uk",
    license="BSD",
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="project django",
    packages=["babik_card_primitives"],
    install_requires = ["django>=1.8,<1.10"],
    tests_require = ["pytest", "pytest-django", "pytest-cov",],
    setup_requires = ["pytest-runner"]
)
