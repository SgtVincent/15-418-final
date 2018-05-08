#!/usr/bin
cd ~
tar xzvf cudnn-9.0-linux-x64-v7.1.tgz
sudo cp cuda/lib64/* /usr/local/cuda/lib64/
sudo cp cuda/include/cudnn.h /usr/local/cuda/include/
rm -rf ~/cuda
rm cudnn-9.0-linux-x64-v7.1.tgz