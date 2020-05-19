import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='django-workspaces',
    version='0.1.0',
    author='Siva Narayanan',
    author_email='siva@fyle.in',
    description='Django starter package for SaaS applications',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',  
    keywords=['django', 'api', 'python', 'sdk'],
    url='https://github.com/snarayanank2/django-workspaces',
    packages=setuptools.find_packages(),
    install_requires=['djangorestframework==3.11.0', 'django-filter==2.2.0', 
        'pyjwt==1.7.1', 'django-filter==2.2.0', 'drf-writable-nested==0.6.0'
],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
