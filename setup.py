from setuptools import setup, find_packages

setup(
    name="coupon_validator",
    version="0.1.0",
    description="A bot for validating coupon codes on e-commerce websites",
    author="AI Validation Bot Team",
    author_email="example@example.com",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[
        "playwright>=1.20.0",
        "asyncio>=3.4.3",
        "urllib3>=1.26.0",
        "transformers>=4.25.1",
        "numpy>=1.22.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)