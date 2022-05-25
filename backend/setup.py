import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='django-saas',
    version='0.1.0',
    author='Siva Narayanan',
    author_email='siva@fylehq.com',
    description='Django starter package for SaaS applications',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',  
    keywords=['django', 'api', 'python', 'sdk'],
    url='https://github.com/snarayanank2/django-saas',
    packages=['saas_framework'],
    install_requires=['djangorestframework==3.11.0', 'django-filter==2.2.0', 
        'pyjwt==2.4.0', 'django-filter==2.2.0', 'django_q==1.2.1', 'django-storages==1.9.1', 'boto3==1.14.7'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
