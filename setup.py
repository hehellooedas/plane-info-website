from setuptools import find_packages,setup

setup(
    name='民航行程推荐',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask=2.1.2',
        'flask-cors',
        'flask-mail',
        'flask-script',
        'flask_seasurf',
        'flask_apscheduler',
        'flask_avatars',
        'pandas'
    ],
)