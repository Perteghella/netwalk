import unittest
from netwalk import Fabric, Switch, Interface

class TestFabricBase(unittest.TestCase):
    def test_cdp_neighborship(self):
        """
        A --- B
        |     |
        C --- D
        """
    
        f = Fabric()
        a = Switch(hostname="A", facts={'hostname': 'A', 'fqdn': 'A.not set'})
        b = Switch(hostname="B", facts={'hostname': 'B', 'fqdn': 'B.not set'})
        c = Switch(hostname="C", facts={'hostname': 'C', 'fqdn': 'C.not set'})
        d = Switch(hostname="D", facts={'hostname': 'D', 'fqdn': 'D.not set'})

        f.switches = {'A': a,
                      'B': b,
                      'C': c,
                      'D': d}

        a.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'B',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = b),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'C',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = c)}

        b.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'A',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = a),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = d)}

        c.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = d),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'A',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = a)}

        d.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'C',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = c),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'B',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = b)}

        f._find_links()
        assert f.switches['A'].interfaces['GigabitEthernet0/0'].neighbors[0] == f.switches['B'].interfaces['GigabitEthernet0/0']
        assert f.switches['A'].interfaces['GigabitEthernet0/1'].neighbors[0] == f.switches['C'].interfaces['GigabitEthernet0/1']
        assert f.switches['B'].interfaces['GigabitEthernet0/0'].neighbors[0] == f.switches['A'].interfaces['GigabitEthernet0/0']
        assert f.switches['B'].interfaces['GigabitEthernet0/1'].neighbors[0] == f.switches['D'].interfaces['GigabitEthernet0/1']
        assert f.switches['C'].interfaces['GigabitEthernet0/0'].neighbors[0] == f.switches['D'].interfaces['GigabitEthernet0/0']
        assert f.switches['C'].interfaces['GigabitEthernet0/1'].neighbors[0] == f.switches['A'].interfaces['GigabitEthernet0/1']
        assert f.switches['D'].interfaces['GigabitEthernet0/0'].neighbors[0] == f.switches['C'].interfaces['GigabitEthernet0/0']
        assert f.switches['D'].interfaces['GigabitEthernet0/1'].neighbors[0] == f.switches['B'].interfaces['GigabitEthernet0/1']

    def test_pathfinding_one_target(self):
        """
        A --- B
        |     |
        C --- D
        Find paths from C to A
        """
    
        f = Fabric()
        a = Switch(hostname="A", facts={'hostname': 'A', 'fqdn': 'A.not set'})
        b = Switch(hostname="B", facts={'hostname': 'B', 'fqdn': 'B.not set'})
        c = Switch(hostname="C", facts={'hostname': 'C', 'fqdn': 'C.not set'})
        d = Switch(hostname="D", facts={'hostname': 'D', 'fqdn': 'D.not set'})

        f.switches = {'A': a,
                      'B': b,
                      'C': c,
                      'D': d}
                      

        a.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'B',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = a),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'C',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = a)}

        b.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'A',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = b),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = b)}

        c.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = c),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'A',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = c)}

        d.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'C',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = d),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'B',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = d)}

        f._find_links()

        paths = f.find_paths(c, [a])
        assert c.interfaces['GigabitEthernet0/0'] in paths[0]
        assert d.interfaces['GigabitEthernet0/1'] in paths[0]
        assert d.interfaces['GigabitEthernet0/0'] in paths[0]
        assert b.interfaces['GigabitEthernet0/0'] in paths[0]
        assert b.interfaces['GigabitEthernet0/1'] in paths[0]
        assert a.interfaces['GigabitEthernet0/0'] in paths[0]

        assert c.interfaces['GigabitEthernet0/1'] in paths[1]
        assert a.interfaces['GigabitEthernet0/1'] in paths[1]

    def test_pathfinding_two_targets(self):
        """
        A --- B
        |     |
        C --- D
        Find paths from C to A or B
        """
    
        f = Fabric()
        a = Switch(hostname="A", facts={'hostname': 'A', 'fqdn': 'A.not set'})
        b = Switch(hostname="B", facts={'hostname': 'B', 'fqdn': 'B.not set'})
        c = Switch(hostname="C", facts={'hostname': 'C', 'fqdn': 'C.not set'})
        d = Switch(hostname="D", facts={'hostname': 'D', 'fqdn': 'D.not set'})

        f.switches = {'A': a,
                      'B': b,
                      'C': c,
                      'D': d}
                      

        a.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'B',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = a),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'C',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = a)}

        b.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'A',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = b),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = b)}

        c.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = c),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'A',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = c)}

        d.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'C',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = d),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'B',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = d)}

        f._find_links()

        paths = f.find_paths(c, [a,b])
        assert c.interfaces['GigabitEthernet0/0'] in paths[0]
        assert d.interfaces['GigabitEthernet0/1'] in paths[0]
        assert d.interfaces['GigabitEthernet0/0'] in paths[0]
        assert b.interfaces['GigabitEthernet0/1'] in paths[0]

        assert not b.interfaces['GigabitEthernet0/0'] in paths[0]
        assert not a.interfaces['GigabitEthernet0/0'] in paths[0]

        assert c.interfaces['GigabitEthernet0/1'] in paths[1]
        assert a.interfaces['GigabitEthernet0/1'] in paths[1]


    def test_pathfinding_two_targets_dead_end(self):
        """
        A --- B
        |     |
        C --- D - E
        Find paths from C to A or B.
        Check E not in path
        """
    
        f = Fabric()
        a = Switch(hostname="A", facts={'hostname': 'A', 'fqdn': 'A.not set'})
        b = Switch(hostname="B", facts={'hostname': 'B', 'fqdn': 'B.not set'})
        c = Switch(hostname="C", facts={'hostname': 'C', 'fqdn': 'C.not set'})
        d = Switch(hostname="D", facts={'hostname': 'D', 'fqdn': 'D.not set'})
        e = Switch(hostname="E", facts={'hostname': 'E', 'fqdn': 'E.not set'})

        f.switches = {'A': a,
                      'B': b,
                      'C': c,
                      'D': d,
                      'E': e}
                      

        a.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'B',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = a),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'C',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = a)}

        b.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'A',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = b),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = b)}

        c.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = c),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'A',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = c)}

        d.interfaces = {'GigabitEthernet0/0': Interface(name='GigabitEthernet0/0',
                                                        neighbors=[{'hostname': 'C',
                                                                    'remote_int': 'GigabitEthernet0/0'}],
                                                        switch = d),
                        'GigabitEthernet0/1': Interface(name='GigabitEthernet0/1',
                                                        neighbors=[{'hostname': 'B',
                                                                    'remote_int': 'GigabitEthernet0/1'}],
                                                        switch = d),
                        'GigabitEthernet0/2': Interface(name='GigabitEthernet0/2',
                                                        neighbors=[{'hostname': 'E',
                                                                    'remote_int': 'GigabitEthernet0/2'}],
                                                        switch = d)}

        e.interfaces = {'GigabitEthernet0/2': Interface(name='GigabitEthernet0/2',
                                                        neighbors=[{'hostname': 'D',
                                                                    'remote_int': 'GigabitEthernet0/2'}],
                                                        switch = d)}

        f._find_links()

        paths = f.find_paths(c, [a,b])
        assert e.interfaces['GigabitEthernet0/2'] not in paths[0]


if __name__ == '__main__':
    unittest.main()