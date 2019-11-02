# Case Study 1: Audio source separation using motion information

To run this jupyter notebook you would require: python, GNU octave and jupyter. Creating a separate environment in Miniconda/Anaconda is highly recommended. Please find below a detailed set of steps to get started. If you already satisfy all of the software requirements, skip to step 6.


   1. Install GNU Octave: https://www.gnu.org/software/octave/download.html. Here are some ways to do so:
      - Linux (Package manager): ```apt install octave or yum install octave```
      - Linux or MacOS (Homebrew): ```brew install octave```
      - Windows: Get installer from aforementioned download link
   2. Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
   3. Create a new conda environment using ```environment.yml``` file
      ```sh
      conda env create -f environment.yml
      ```
   4. Activate the environment
      ```sh
      conda activate ismir2019
      ```
   5. Get the code and enter the case study directory
      ```sh
      git clone <repository_link>
      cd <case_study_directory>
      ```
   6. If you have not used ```environment.yml``` please verify that you have all packages listed in that file installed, especially ```oct2py``` python package.
      ```sh
      pip install oct2py
      ```
      or
      ```sh
      conda install -c conda-forge oct2py
      ```
      
   7. Start the jupyter server and open the notebook
      ```sh
      jupyter notebook
      ```
