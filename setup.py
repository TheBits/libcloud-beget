import textwrap

import setuptools

long_description = """
[Libcloud](https://libcloud.apache.org/) driver for provdier beget.com.

For all available methods, see [README at github](https://github.com/thebits/libcloud-beget).
"""


setuptools.setup(
    name="libcloudbeget",
    version="0.0.1",
    author="Sergey Mezentsev",
    author_email="thebits@yandex.ru",
    description="Libcloud driver for provdier beget.com",
    license="UNLICENSE",
    long_description=textwrap.dedent(long_description),
    long_description_content_type="text/markdown",
    url="https://github.com/thebits/libcloud-beget",
    install_requires=["apache-libcloud>=3.0.0"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Systems Administration",
    ],
)
