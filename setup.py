from setuptools import setup, find_packages

setup(
    name='j_juniper',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'weaviate-client',
        'langchain',
        
    ],
    entry_points={
        'console_scripts': [
            'j-juniper=j_juniper.cli:cli',
        ],
    },
)
