from setuptools import setup

setup(name='pymasker',
      version='0.4.0',
      description='python package for mask generation from landsat 8 Quality Assessment band and MODIS land products.',
      url='https://github.com/haoliangyu/pymasker',
      author='Haoliang Yu',
      author_email='haoliang.yu@outlook.com',
      license='MIT',
      py_modules=['pymasker'],
      entry_points={
          "console_scripts": ['pymasker = pymasker:main']
      },
      install_requires=['numpy', 'gdal'],
      zip_safe=False)
