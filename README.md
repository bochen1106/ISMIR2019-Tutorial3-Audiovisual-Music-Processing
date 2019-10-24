
# Skeleton Pianist

**This code is for ISMIR2019 tutorial: "Audiovisual Music Processing"**

- This is a simplified version of the paper:
Bochen Li, Akira Maezawa, and Zhiyao Duan, "**Skeleton plays piano: online generation of pianist body movements from MIDI performance**", in *Proc., International Society for Music Information Retrieval*, 2018.
- The code will generate a pianist body skeleton movements as a video file given input of MIDI files.
- More details can be found [HERE](http://www.ece.rochester.edu/projects/air/projects/skeletonpianist.html).

## Requirements

Assuming conda environment

`conda install ffmpeg`

`pip install chainer==3.0.0`

`conda install -c conda-forge numpy`

`pip install opencv-python`

`pip install pretty_midi`

`pip install librosa`

## How to Run

`python run.py "example/Mozart_K545_Ch2.mid"`

It will generate the output video in the `output` folder
(A pre-generated video is already saved there)


![alt text](https://www.youtube.com/watch?v=JJcwV9cZiUY)
