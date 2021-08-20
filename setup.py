import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name='twarc-hashtags',
    version='0.0.4',
    url='https://github.com/docnow/twarc-hashtags',
    author='Ed Summers',
    author_email='ehs@pobox.com',
    py_modules=['twarc_hashtags'],
    description='A twarc plugin to extract hashtags from Twitter data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.3',
    install_requires=['twarc>=2.1.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points='''
        [twarc.plugins]
        hashtags=twarc_hashtags:hashtags
    '''
)
