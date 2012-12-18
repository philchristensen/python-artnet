from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
	name = "python-artnet",
	version = "0.1",
	
	include_package_data	= True,
	zip_safe				= False,
	packages				= find_packages('src'),
	package_dir				= {'': 'src'},
	
	entry_points	= {
		'setuptools.file_finders'	: [
			'git = setuptools_git:gitlsfiles',
		],
		'console_scripts': [
			'artnet_listener = artnet.listener:main',
			'artnet_blackout = artnet.scripts.blackout:main',
			'artnet_halfup = artnet.scripts.halfup:main',
			'artnet_strobe = artnet.scripts.strobe:main',
			'artnet_test_fixture = artnet.scripts.test_fixture:main',
		]
	},
	
	install_requires = open('requirements.txt', 'rU')
)