import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'pinakin',
    packages=setuptools.find_packages(),
    version = '0.2',
    include_package_data=True,
    description = 'Unofficial Python Wrapper library for Multiple Indian Brokers',
    long_description=long_description,
    long_description_content_type="text/markdown",  author = 'Aeron7',
    author_email = 'dexter@unofficed.com',
    url = 'https://unofficed.com',
    install_requires=['requests', 'pandas','curlify'],
    keywords = ['upstox', 'uplink', 'python', 'nse', 'trading', 'stock markets'],
    classifiers=[
      'Intended Audience :: Developers',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: Implementation :: PyPy',
      'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
