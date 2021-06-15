
python3 -m pip install numpy scipy matplotlib cython pandas pyqt5 wheel vtk twine setuptools_rust cryptography==3.3.2 auditwheel

COPY . ./temporary/PyMieSim/

rm -rf /temporary/PyMieSim/CMakeFiles /GitProject/PyMieSim/CMakeCache.txt

mkdir /temporary/PyMieSim/output /temporary/PyMieSim/dist/* /temporary/PyMieSim/build/* /temporary/PyMieSim/output/*

rm /temporary/PyMieSim/**/*.so /temporary/PyMieSim/**/**/*.so -f

cp -r /temporary/PyMieSim/extern/math/include/boost /usr/include

mkdir /temporary/PyMieSim/extern/complex_bessel/build

cd /temporary/PyMieSim/extern/complex_bessel/build && cmake -DBUILD_TESTING=OFF .. && make install

cd ../../../..

cd /temporary//PyMieSim && cmake . && make clean && make all

cd /temporary/PyMieSim && python3 -m pip install -r requirements.txt

cd /temporary/PyMieSim/ && python3 setup.py install

cd /temporary/PyMieSim/ && python3 setup.py bdist_wheel

auditwheel repair /temporary/PyMieSim/dist/*.whl -w /temporary/PyMieSim/output
