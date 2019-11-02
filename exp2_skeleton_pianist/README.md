
# Skeleton Pianist

**This code is for ISMIR2019 tutorial: "Audiovisual Music Processing"**

- This is a simplified version of the paper:
Bochen Li, Akira Maezawa, and Zhiyao Duan, "**Skeleton plays piano: online generation of pianist body movements from MIDI performance**", in *Proc., International Society for Music Information Retrieval*, 2018.
- The code will generate a pianist body skeleton movements as a video file given input of MIDI files.
- More details and demos can be found [HERE](http://www.ece.rochester.edu/projects/air/projects/skeletonpianist.html).

## Requirements
(skip this if already installed environment.yml in root folder)
Assuming conda environment
- `conda install ffmpeg`
- `pip install chainer==3.0.0`
- `pip install opencv-python`
- `pip install pretty_midi`
- `pip install librosa`

## Folder Structure

- `data` Model files, background canvas image, and scaling factor for skeleton plot
- `example` Some sample MIDI files to try out
- `output` The output folder for the generated videos

## How to Run

`python run.py "example/Mozart_K545_Ch2.mid"`

It will generate the output video in the `output` folder
(A pre-generated video is already saved there)

Also start your code in `try_more_variations.py` to observe how the generated skeleton movements differ by modifying some MIDI note properties.

You can also try creating some MIDI input (e.g., Logic Pro) and feed into the model.

