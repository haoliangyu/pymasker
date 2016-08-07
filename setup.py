from setuptools import setup

setup(name='pymasker',
      version='0.3.0',
      description='python package for mask generation from landsat 8 Quality Assessment band and MODIS land products.',
      url='https://github.com/haoliangyu/pymasker',
      author='Haoliang Yu',
      author_email='haoliang.yu@outlook.com',
      license='MIT',
      py_modules=['pymasker'],
      install_requires=['numpy',],
      zip_safe=False)
