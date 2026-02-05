"""
FinSight AI - SME Financial Intelligence Platform
Setup configuration for package installation
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name='finsight-ai',
    version='1.0.0',
    author='FinSight AI Team',
    author_email='support@finsight.ai',
    description='SME Financial Intelligence Platform with AI-powered insights',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/financial-health-platform',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Accounting',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Framework :: FastAPI',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-cov>=4.1.0',
            'black>=23.12.0',
            'flake8>=6.1.0',
            'mypy>=1.7.1',
        ],
        'docs': [
            'sphinx>=7.2.6',
            'sphinx-rtd-theme>=2.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'finsight-analyze=scripts.run_analysis:main',
            'finsight-report=scripts.generate_report:main',
            'finsight-server=uvicorn src.api.routes:app',
        ],
    },
    include_package_data=True,
    package_data={
        'config': ['*.yaml', '*.json'],
    },
    zip_safe=False,
    keywords='sme finance credit-scoring forecasting ai machine-learning',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/financial-health-platform/issues',
        'Documentation': 'https://docs.finsight.ai',
        'Source': 'https://github.com/yourusername/financial-health-platform',
    },
)