
# ISMIR2019 Tutorial 3: Audiovisual Music Processing
This repository contains slides, code and additional material for ISMIR 2019 tutorial on Audiovisual music processing.

## Environment setup
It is highly recommended to use a separate Miniconda/Anaconda environment to run the tutorial case studies. In addition, for ```exp1``` you would require a GNU Octave and jupyter installation.  Please find below a detailed set of steps to get started. If you already satisfy all of the software requirements you can directly start with the instructions in corresponding case study folders.


1. Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
2. Install GNU Octave (Required for ```exp1```): https://www.gnu.org/software/octave/download.html. Here are some ways to do so:
      - Linux (Package manager): ```apt install octave or yum install octave```
      - Linux or MacOS (Homebrew): ```brew install octave```
      - Windows: Get installer from aforementioned download link

   **Note**: Please ensure that GNU Octave is in your PATH. For Windows users, it might be easier to set the OCTAVE_EXECUTABLE environment variable with the path to your octave executable. For example, this could be: ```C:\Octave-5.1.0.0\mingw64\bin\octave-cli.exe```
3. Get the code
   ```sh
   git clone <repository_link>
   ```
4. Create a new conda environment using ```environment.yml``` file
   ```sh
   conda env create -f environment.yml
   ```
   **Note**: For anyone encountering the ```PackageNotFoundError``` with ```ffmpeg``` install:
      - First, remove the line ```- ffmpeg``` from environment.yml
      - After creating and activating ismir2019 environment, do 
	```sh
        conda install -c conda-forge ffmpeg
	```
5. Activate the environment
   ```sh
   conda activate ismir2019
   ```
You are now ready to run the experiments!
   


