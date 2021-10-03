conda create --name tf15 python=3.8
conda activate tf15
#conda install -c conda-forge tensorflow-gpu=1.15
#conda install -c conda-forge tensorboardx -y
#conda install -c conda-forge notebook -y
#conda install -c conda-forge numpy=1.16.6 -y
#conda install -c conda-forge pandas -y
#conda install -c conda-forge matplotlib -y
#conda install -c conda-forge opencv -y
#conda install -c conda-forge scikit-learn -y
#conda install -c conda-forge tqdm -y
#conda install -c conda-forge scikit-image -y
#conda install -c anaconda scipy=1.5.3 -y
#conda install -c anaconda h5py=2.10.0 -y
apt-get -y install cmake libopenmpi-dev python3-dev zlib1g-dev libgl1-mesa-dev
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install -r ../app/requirements.txt
pip3 install tensorboard