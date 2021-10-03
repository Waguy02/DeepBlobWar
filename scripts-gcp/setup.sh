conda create --name tf1 python=3.7
conda activate tf1
conda install -c conda-forge tensorflow-gpu=1.15
conda install -c conda-forge tensorboardx -y
conda install -c conda-forge notebook -y
conda install -c conda-forge numpy=1.16.6 -y
conda install -c conda-forge pandas -y
conda install -c conda-forge matplotlib -y
conda install -c conda-forge opencv -y
conda install -c conda-forge scikit-learn -y
conda install -c conda-forge tqdm -y
conda install -c conda-forge scikit-image -y
conda install -c anaconda scipy=1.5.3 -y
conda install -c anaconda h5py=2.10.0 -y

conda install stable-baselines[mpi]==2.10.1
conda install jupyter==1.0.0
conda install jupyterlab==3.0.0
conda install pillow
