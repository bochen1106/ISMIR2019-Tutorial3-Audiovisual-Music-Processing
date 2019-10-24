
"""
Created on Tue Oct 22 13:01:06 2019

@author: bochenli
"""


import sys
import os
import numpy as np
import function
import librosa
import cv2
from model import Model

filename_model = "data/model"
filename_canvas = "data/canvas.png"
filename_scale_factor = "data/scale_factor.txt"
path_out = "./output"
frame_buffer = 30


def main(filename_midi):
    
    
    print ("read midi into pianoroll representation ...")
    notes = function.read_midi(filename_midi)
    #notes = notes[:200, ...]
    pianoroll = function.get_pianoroll(notes)
    n_frame = pianoroll.shape[1]
    print ("total number of frames: %d" % n_frame)
    
    
    print ("prepare samples as model input ...")
    x = []
    for fnum in range(frame_buffer, n_frame-frame_buffer):
        x.append(pianoroll[:, fnum-frame_buffer : fnum+frame_buffer][None, :, :])
    x = np.asarray(x, dtype='float32')
    print ("total number of samples: %d" % len(x))
    
    
    print ("load model from: %s" % filename_model)
    model = Model()
    model.load(filename_model)
    model.reset()
    
    
    
    print ("model inference ...")
    y = []
    for _x in x:
        y.append(model(_x[None,:]).data)
    y = [tmp.ravel() for tmp in y]
    y = np.array(y)


    print ("scale the generated skeleton to real coordinates")
    y = function.smo_pose(y, 7)
    y_dumb = np.zeros((frame_buffer, 16))
    y = np.concatenate((y_dumb, y, y_dumb), axis=0)
    y = [a.reshape(8, 2) for a in y]
    para = np.loadtxt(filename_scale_factor)
    y = function.recover_pose(y, para)
    
    
    print ("generate the output video with the synthesized sound ...")
    name = os.path.basename(filename_midi).rsplit(".", 1)[0]
    
    filename_video = os.path.join(path_out, name+".mp4")
    canvas = cv2.imread("data/canvas.png")
    canvas = canvas[:,:,[2,1,0]]
    function.write_video_pose_background(filename_video, y, notes, canvas)
    
    filename_audio = os.path.join(path_out, name+".wav")
    wave_out = function.syn_midi(notes, fs=44100)
    librosa.output.write_wav(filename_audio, wave_out, 44100)
    function.add_audio_to_video(filename_video, filename_audio)
    os.remove(filename_audio)
    
    


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        filename_midi = sys.argv[1]
    else:
        filename_midi = "example/Mozart_K545_Ch2.mid"
    
    main(filename_midi)












