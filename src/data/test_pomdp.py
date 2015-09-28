import pomdp
import unittest

class TestPomdp(unittest.TestCase):

#  def test_isupper(self):
#      self.assertTrue('FOO'.isupper())
#      self.assertFalse('Foo'.isupper())
#
#  def test_split(self):
#      s = 'hello world'
#      self.assertEqual(s.split(), ['hello', 'world'])
#      # check that s.split fails when the separator is not a string
#      with self.assertRaises(TypeError):
#          s.split(2)

    def test_1(self):
        P = pomdp.pomdp(
            ['s0','s1','s2'],
            ['a','b'],
            {
                ('s0','a'): {'s0': 0, 's1': 0.2, 's2': 0.8},
                ('s0','b'): {'s0': 0, 's1': 0.4, 's2': 0.6}
            },
            ['o1','o2'],
            {
                's0': {'o1': 0.5, 'o2': 0.5},
                's1': {'o1': 0.5, 'o2': 0.5},
                's2': {'o1': 0.3, 'o2': 0.7}
            }
        )      
        self.assertEqual(P.T[('s0','a')]['s1'], 0.2)



if __name__ == '__main__':
    unittest.main()