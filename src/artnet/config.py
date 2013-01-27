from artnet import fixtures

def get_default_fixture_group(config):
	fixture_index = dict()
	group_index = dict()
	for section in config.sections():
		if(section.startswith('fixture_')):
			address = config.get(section, 'address')
			fixturedef = config.get(section, 'fixturedef')
			found[section] = fixtures.Fixture.create(address, fixturedef)
	# 	g = fixtures.FixtureGroup([
	# 	fixtures.Fixture.create(420, 'chauvet/slimpar-64.yaml'),
	# 	fixtures.Fixture.create(427, 'chauvet/slimpar-64.yaml'),
	# 	fixtures.Fixture.create(434, 'chauvet/slimpar-64.yaml'),
	# 	fixtures.Fixture.create(441, 'chauvet/slimpar-64.yaml'),
	# ])

	