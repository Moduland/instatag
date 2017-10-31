from distutils.core import setup
setup(
  name = 'instatag',
  packages = ['instatag'],
  version = '0.1',
  description = 'Extract users from tag in instagram',
  long_description="",
  author = 'Moduland Co',
  author_email = 'info@moduland.ir',
  url = 'https://github.com/Moduland/instatag',
  download_url = 'https://github.com/Moduland/instatag/tarball/v0.1',
  keywords = ['extract', 'scrap', 'instagram','python','tags','users'],
  install_requires=[
      'art',
      'bs4',
      'requests',
      ],
  classifiers = [],
  license='MIT',
)
