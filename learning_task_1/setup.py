from setuptools import find_packages, setup

package_name = 'learning_task_1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rafee',
    maintainer_email='rafee2587@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "count_node = learning_task_1.count_node:main",
            "number_node = learning_task_1.number_node:main",
            "turtle_D = learning_task_1.turtle_D:main",
            "turtle_sequence = learning_task_1.turtle_sequence:main"
        ],
    },
)
