import unittest
import sys
sys.path.insert(0, '../')
import Atlantis
import GGlib
import os

class GhostGearTests(unittest.TestCase):
	
	def testExtractAndWriteCsv(self):
		db = Atlantis.GGDB()
		self.assertIsInstance(db, Atlantis.GGDB)
		result = db.extractSHP("acpg", "'Baie_des_chaleurs'")
		self.assertEqual(len(result),5)
		GGlib.write_points_2csv(result,"test")
		self.assertTrue(os.path.isfile("./test.csv"))
		
	def testCSVfileOK(self):
		#ToDo
		pass;
if __name__ == '__main__':
    unittest.main()
