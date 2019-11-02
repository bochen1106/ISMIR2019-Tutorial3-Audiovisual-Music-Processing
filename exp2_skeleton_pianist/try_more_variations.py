"""
Created on Sat Nov  2 00:02:43 2019

@author: bochen
"""

import function
import run

# change the tempo

filename_in = "example/Bach_FrenchSuite_1.mid"
filename_out = "example/Bach_FrenchSuite_1_tempo1.5.mid"
function.modify_midi_tempo(filename_in, filename_out, 1.5)

run.main(filename_in)


'''
# change the pitch

filename_in = "example/Bach_FrenchSuite_1.mid"
filename_out = "example/Bach_FrenchSuite_1_pitch+15.mid"
function.modify_midi_pitch(filename_in, filename_out, 15)

run.main(filename_out)
'''


