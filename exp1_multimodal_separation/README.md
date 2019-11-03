# Case Study 1: Audio source separation using motion information

This case study will introduce participants to audio-visual source separation in the Nonnegative Matrix Factorization (NMF) framework. Specifically, we provide an illustrative example based on (Parekh et al. 2017). This utilizes a recording from the URMP dataset (). Motion segments were extracted using a multicuts algorithm ().

## Setup
If you have setup your environment as described in repository's ```README.md``` you can simply start the jupyter server and open the notebook. If not, please verify that you have GNU Octave and python packages listed in ```requirements.txt```, especially ```oct2py```, installed.
	- To install ```librosa```
      ```sh
      pip install librosa
      ```
      or
      ```sh
      conda install -c conda-forge librosa
      ```
   - To install ```oct2py```
      ```sh
      pip install oct2py
      ```
      or
      ```sh
      conda install -c conda-forge oct2py
      ```
      
   - To start the jupyter server
      ```sh
      jupyter notebook
      ```
	  
## References
- (Parekh et al. 2017) Parekh, S., Essid, S., Ozerov, A., Duong, N. Q., Pérez, P., & Richard, G. (2017, October). Guiding audio source separation by video object information. In IEEE  Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA), 2017.
- (Li et al. 2018) Bochen Li *, Xinzhao Liu *, Karthik Dinesh, Zhiyao Duan, Gaurav Sharma, Creating a multi-track classical music performance dataset for multi-modal music analysis: Challenges, insights, and applications. In IEEE Transactions on Multimedia, 2018.
- (Keuper et al. 2015) M. Keuper, B. Andres, and T. Brox, Motion trajectory segmentation via minimum cost multicuts. In IEEE International Conference on Computer Vision (ICCV), 2015.
