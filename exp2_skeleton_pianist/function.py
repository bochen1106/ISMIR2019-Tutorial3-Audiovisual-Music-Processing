
"""
Created on Tue Oct 22 21:38:36 2019

@author: bochenli
"""

import os
import numpy as np
import math
import cv2
import pretty_midi

FPS = 30        # frame rate (frame per second)

'''
read a MIDI file into a note matrix

input: 
    
    - notes:        shape=(n, 4)
                    each row represents: onset(sec), offset(sec), pitch(MIDInumber), velocity
                
    - frame_hop:    the frame hop to quantize MIDI time (default: 1/FPS)
                
output:
    
    - pianoroll:    pianoroll representation, shape=(128, n_frame)
'''    
def get_pianoroll(notes, frame_hop=1/FPS):

    onset = notes[:, 0]
    offset = notes[:, 1]
    pitch = notes[:, 2]
    
    dur_total = max(offset)
    n_frame = int( dur_total / frame_hop)

    pianoroll = np.zeros((128, n_frame))
    onset = ( onset / frame_hop ).astype('i')
    offset = ( offset / frame_hop ).astype('i')
    for k in range(128):
        idx = np.where(pitch==k)[0]
        for i in idx:
            pianoroll[k, onset[i] : offset[i]] = 1
   
    return pianoroll



'''
smooth the pose data

input:
    
    - pose:         np.array, shape=(n_frame, 16)
    - win_size:     the sliding window size
    
input:
    
    - pose:         np.array, shape=(n_frame, 16)
    
'''
def smo_pose(pose, win_size=9):
    
    for i in range(pose.shape[1]):
        p = pose[:, i]
        p = np.convolve(p, np.ones(win_size)/win_size, "same")
        pose[:, i] = p
        
    return pose
    
'''
recover the pose data to real coornidate from normalized data
'''
def recover_pose(pose, para):
    
    m_x, m_y, std = para

    pose = np.asarray(pose).astype('f')
    pose *= std
    pose[:,:,1] += m_y
    pose[:,:,0] += m_x
    pose = np.asarray(pose).astype('i')
        
    return pose


'''
plot one frame of pose data
       
    - input:
    
        - pose:         pose coordinates, shape=(8, 2)
        
        - img:          the background image
                        (if None, create a new gray canvas)
                        
        - plot_hand:    plot a hand position or not
    
    - output:
    
        - canvas:       the plotted canvas with the pose visualization
        
'''
def plot_pose(pose, img=None, plot_hand=True):
    
    if img is None:
        canvas = np.ones((480, 720, 3), dtype='uint8')*200
    else:
        canvas = img
    
    limb = np.asarray([
            [0,1],
            [1,2],
            [2,3],
            [3,4],
            [1,5],
            [5,6],
            [6,7]
            ], dtype='i')
    
    color_joint = [
    [255, 0, 0], 
    [255, 0, 0], 
    [0, 0, 255],  
    [0, 0, 255], 
    [0, 0, 255], 
    [0, 180, 0], 
    [0, 180, 0], 
    [0, 180, 0]]
   
    pose_fnum = pose
    n_joint = len(color_joint)
    n_limb = len(limb)
    

    for i in range(n_limb):
        [x1, y1] = [pose_fnum[limb[i,0], 0], pose_fnum[limb[i,0], 1]]
        [x2, y2] = [pose_fnum[limb[i,1], 0], pose_fnum[limb[i,1], 1]]
        cv2.line(canvas, (int(x1),int(y1)),(int(x2),int(y2)), [255,255,255], 2)         
    
    for i in range(n_joint):
        x = int(pose_fnum[i, 0])
        y = int(pose_fnum[i, 1])
        cv2.circle(canvas, tuple([x,y]), 8, color_joint[i], thickness=-1) 

    if plot_hand:
        color_hand = [255,255,0]
        canvas_cur = canvas.copy()
        pos_hand_1 = ( 1.45 * pose_fnum[4,:] - 0.45 * pose_fnum[3,:] ).astype('i')
        pos_hand_2 = ( 1.45 * pose_fnum[7,:] - 0.45 * pose_fnum[6,:] ).astype('i')
        l1 = int( ((pose_fnum[4,0] - pose_fnum[3,0]) ** 2 + (pose_fnum[4,1] - pose_fnum[3,1]) ** 2) ** 0.5 )
        l2 = int( ((pose_fnum[7,0] - pose_fnum[6,0]) ** 2 + (pose_fnum[7,1] - pose_fnum[6,1]) ** 2) ** 0.5 )
        angle1 = math.degrees(math.atan2(pose_fnum[4,1] - pose_fnum[3,1], pose_fnum[4,0] - pose_fnum[3,0]))
        angle2 = math.degrees(math.atan2(pose_fnum[7,1] - pose_fnum[6,1], pose_fnum[7,0] - pose_fnum[6,0]))
        polygon1 = cv2.ellipse2Poly(tuple(pos_hand_1), (int(l1/3), 18), int(angle1), 0, 360, 1)
        polygon2 = cv2.ellipse2Poly(tuple(pos_hand_2), (int(l2/3), 18), int(angle2), 0, 360, 1)

        cv2.fillConvexPoly(canvas_cur, polygon1, color_hand)
        cv2.fillConvexPoly(canvas_cur, polygon2, color_hand)
        canvas = cv2.addWeighted(canvas, 0.4, canvas_cur, 0.6, 0)
    
    return canvas



'''
read a MIDI file into a note matrix

input:
    
    - filename: the filename (full path) of the MIDI file
    
output: 
    
    - notes:    shape=(n, 4)
                each row represents: onset(sec), offset(sec), pitch(MIDInumber), velocity
'''
def read_midi(filename):
    
    midi_data = pretty_midi.PrettyMIDI(filename)
    instrument = midi_data.instruments[0]
    
    n_note = len(instrument.notes)
    notes = np.zeros((n_note, 4))
    
    for i in range(n_note):
        note_event = instrument.notes[i]
        notes[i] = note_event.start, note_event.end, note_event.pitch, note_event.velocity
    
    return notes


'''
write a note matrix into a MIDI file

input: 
    
    - notes:    shape=(n, 4)
                each row represents: onset(sec), offset(sec), pitch(MIDInumber), velocity
                
output:
    
    - filename: the filename (full path) of the MIDI file
    
'''
def write_midi(filename, notes):
    
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program("Acoustic Grand Piano"))
    
    for note in notes:
        note = pretty_midi.Note(velocity=int(note[3]), pitch=int(note[2]), start=note[0], end=note[1])
        piano.notes.append(note)
        
    midi.instruments.append(piano)
    midi.write(filename)


'''
synthesize the MIDI as wave

input:

    - notes:            shape=(n, 4)
                        each row represents: onset(sec), offset(sec), pitch(MIDInumber), velocity
    
    - fs:               the sample rate
    
    - real_duration:    True (use real note duration), or
                        False (use 0.1sec for all notes as staccatos)
                        
    - real_volume:      True (use real note volume), or
                        False (use 100 for all notes)
    
output:
    
        - wave_out:     the synthesized waveform
        
'''
def syn_midi(notes, fs=44100, real_duration=True, real_volume=True):
    
    n_note = notes.shape[0]
    onset = notes[:, 0]
    offset = notes[:, 1]
    pitch = notes[:, 2]
    volume = notes[:, 3]
    
    if real_volume:
        volume = volume
    else:
        volume = np.ones(n_note) * 100
        
    if real_duration:
        duration = offset - onset
    else:
        duration = np.ones(n_note) * 0.1
    
    piece_dur = max(offset)
    
    # vector for output waveform
    tt = np.arange(0, piece_dur, 1.0/fs)
    
    def syn_note(pit, dur, fs, num_harm=12):
        
        # syntheszie one note
        
        if pit == 0:
            return np.asarray([0])
        dur = max(0.025, dur)
        dur = min(5, dur)
        freq = np.power(2, (pit-69)/12.0) * 440
        t = np.arange(0, dur, 1.0/fs)
        wav = np.zeros(t.size)
        
        partials = np.arange(freq, min(freq*(num_harm+1), fs/2), freq)
        ampl = 1.0 / np.power(1.5, range(len(partials)))
        for i in range(len(partials)):
            wav += ampl[i] * np.sin( 2*np.pi*partials[i]*t )
        
        # build a coarse envelope
        envelope = np.flip(np.arange(0, 1, 1/fs/5)) ** 2  # envelope decay 5 sec
        envelope = envelope[:t.size]
        ramp = 0.01
        idx = int(ramp*fs)
        ramp = np.arange(0, 1, 1/idx)
        envelope[:idx] *= ramp
        envelope[-idx:] *= np.flip(ramp)
        
        wav *= envelope

        return wav

    # convert each note to a waveform, then sum up
    wave_out = np.zeros(tt.size)

    for i in range(n_note):
        wav = syn_note(pitch[i], duration[i], fs)
        idx = int(onset[i]*fs)
        wave_out[idx:idx+len(wav)] += wav * volume[i]
    rms =  np.sqrt(np.mean(wave_out**2))  
    wave_out = wave_out/rms * 0.05
    
    return wave_out



'''
add soundtrack to video (call system command line operation, ffmpeg required)
'''
def add_audio_to_video(filename_video, filename_audio, filename_video_out=None):
        
    if not filename_video_out:
        filename_video_out = filename_video.rsplit(".", 1)[0] + "_final.mp4"
        
    command = 'ffmpeg  -i "%s" -i "%s" -c:v copy  -c:a aac  "%s" -strict -2  -shortest -y -v 0' % (
            filename_audio, filename_video, filename_video_out)

    os.system(command)

    

'''
generate output video (silent) for skeleton movements
'''
def write_video_pose_background(filename, y, notes, img):
    
    if not os.path.exists( os.path.dirname(filename) ):
        os.makedirs(os.path.dirname(filename))
    
#    fourcc = cv2.VideoWriter_fourcc(*'H264')
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    vid_out = cv2.VideoWriter(filename, fourcc, FPS, (720, 480))

    n_frame = len(y)
    for fnum in range(n_frame):
        canvas = plot_pose(y[fnum], img.copy())
        vid_out.write(canvas[:,:,[2,1,0]])
    vid_out.release()
    
'''
modify the tempo of a given MIDI file

Input:
    
    - scale:        scale factor of the tempo, e.g., scale=1.2 will change tempo from 100 BPM to 120 BPM

'''
def modify_midi_tempo(filename_in, filename_out, scale):
    
    notes = read_midi(filename_in)
    notes[:, :2] /= scale
    write_midi(filename_out, notes)    


'''
modify the pitch for all the notes of a given MIDI file

Input:
    
    - semitone:     the difference of pitch change, e.g., semitone=12 will rise one octave of the piece

'''
def modify_midi_pitch(filename_in, filename_out, semitone):
    
    notes = read_midi(filename_in)
    notes[:, 2] += semitone
    notes[:, 2] = [x if x<108 else 108 for x in notes[:, 2]]
    notes[:, 2] = [x if x>21 else 21 for x in notes[:, 2]]
    write_midi(filename_out, notes)      
                       
                       
                       
                       
                       
                       
                       
                       