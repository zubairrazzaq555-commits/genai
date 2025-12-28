from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Zubair Ahmed',
    author_email='zubairrazzaq555@gmail.com',  # Fixed typo
    install_requires=[
        'openai',
        'langchain',       # Fixed typo
        'langchain-openai',
        'streamlit',
        'python-dotenv',   # Fixed typo
        'pypdf'            # Recommended over pyPDF2
    ],
    packages=find_packages()
)
