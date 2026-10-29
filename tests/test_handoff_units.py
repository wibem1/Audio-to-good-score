"""Standard-library regression cases for protocol 0.2, not a complete validator."""
from fractions import Fraction as F
import unittest

def seconds(pulse_q,bpm,ref_q):return 60*pulse_q/(bpm*ref_q)
def xml_duration(q,divisions):
 n=q*divisions
 if n.denominator!=1:raise ValueError('insufficient divisions')
 return int(n)
class Units(unittest.TestCase):
 def test_quarter_tempo(self):self.assertEqual(seconds(F(1,4),F(7500,89),1),F(89,500))
 def test_dotted_tempo(self):self.assertEqual(seconds(F(1,4),F(5000,89),F(3,2)),F(89,500))
 def test_gemini_wrong_midi_tempo(self):self.assertNotEqual(seconds(F(1,4),84,F(3,2)),F(89,500))
 def test_xml_sixteenth(self):self.assertEqual(xml_duration(F(1,4),480),120)
 def test_reject_divisions_two(self):
  with self.assertRaises(ValueError):xml_duration(F(1,4),2)
 def test_overfull_68(self):self.assertNotEqual(F(12,2),F(6*4,8))
 def test_full_68(self):self.assertEqual(12*F(1,4),F(6*4,8))
 def test_dotted_half(self):self.assertEqual(xml_duration(F(3),480),1440)
 def test_triplet(self):self.assertEqual(xml_duration(F(1,3),480),160)
 def test_midi_rounding(self):
  mpq=round(F(60000000)/F(7500,89));self.assertEqual(mpq,712000);self.assertEqual(F(mpq,1000000)/4,F(89,500))
 def test_gate_is_not_notated_duration(self):self.assertNotEqual(F(115,480),F(1,4))
 def test_tempo_display_and_sound(self):self.assertEqual(F(5000,89)*F(3,2),F(7500,89))
if __name__=='__main__':unittest.main()
