
# ISMIR2019 Tutorial 3: Audiovisual Music Processing
This repository contains slide, code and additional material for ISMIR 2019 tutorial on Audiovisual music processing.

## Environment setup
It is highly recommended to use a separate Miniconda/Anaconda environment to run the tutorial case studies. In addition, for ```exp1``` you would require a GNU Octave and jupyter installation.  Please find below a detailed set of steps to get started. If you already satisfy all of the software requirements you can directly start with the instructions in corresponding case study folders.


1. Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
2. Install GNU Octave (Required for ```exp1```): https://www.gnu.org/software/octave/download.html. Here are some ways to do so:
      - Linux (Package manager): ```apt install octave or yum install octave```
      - Linux or MacOS (Homebrew): ```brew install octave```
      - Windows: Get installer from aforementioned download link
3. Get the code
   ```sh
   git clone <repository_link>
   ```
4. Create a new conda environment using ```environment.yml``` file
   ```sh
   conda env create -f environment.yml
   ```
5. Activate the environment
   ```sh
   conda activate ismir2019
   ```
You are now ready to run the experiments!
   


