
python3 -m pip install numpy scipy matplotlib cython pandas pyqt5 wheel vtk twine setuptools_rust cryptography==3.3.2 auditwheel delocate

export TMP=~/temporary/PyMieSim

sudo cp -r . $TMP

sudo rm -rf $TMP/CMakeFiles ~/GitProject/PyMieSim/CMakeCache.txt

sudo mkdir $TMP/output $TMP/dist/* $TMP/build/* $TMP/output/*

sudo rm $TMP/**/*.so $TMP/**/**/*.so -f

sudo cp -r $TMP/extern/math/include/boost /usr/include

sudo mkdir $TMP/extern/complex_bessel/build

cd $TMP/extern/complex_bessel/build && cmake -DBUILD_TESTING=OFF .. && make install

cd ../../../..

export CMAKE_C_COMPILER=gcc-11
export CMAKE_CXX_COMPILER=g++-11

cd $TMP && cmake . && make clean && make all

cd $TMP && python3 -m pip install -r requirements.txt

cd $TMP && python3 setup.py install

cd $TMP && python3 setup.py bdist_wheel

sudo delocate-wheel $TMP/dist/*.whl -w $TMP/output
