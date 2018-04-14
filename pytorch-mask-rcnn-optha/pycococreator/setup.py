from distutils.core import setup
from distutils.extension import Extension

# To install library to Python site-packages run "python setup.py  install"

setup(name='pycococreatortools',
    packages=['pycococreatortools'],
    package_dir = {'pycococreatortools': 'pycococreatortools'},
    version='0.1.1',
    description = 'Tools to create COCO datasets',
    url = 'https://github.com/waspinator/pycococreator',
    author = 'waspinator',
    author_email = 'patrickwasp@gmail.com',
    download_url = 'https://github.com/waspinator/pycococreator/archive/0.1.1.tar.gz',
    keywords = ['coco', 'dataset', 'machine-learning'],
    install_requires=[
        'numpy', 'pillow', 'skimage'
    ],
)
