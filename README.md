# Trace2Model
A framework to learn system models from system execution traces.

# Setup Instructions

## Fedora

Install Basic Requirements

~~~
dnf groupinstall "Development Tools"
dnf install kernel-devel kernel-headers
dnf install gcc gcc-c++ flex bison perl-libwww-perl patch git
~~~

Install Tool Dependencies
~~~
yum install python3
yum install cvc4
yum install z3
~~~

Cloning Fastsynth
~~~
git clone https://github.com/kroening/fastsynth.git
cd fastsynth
git reset --hard b8841e05ef97a35d28fb097fa0e19cc998021997
git submodule init
git submodule update
~~~

Building CBMC
~~~
cd fastsynth/lib/cbmc
make -C src minisat2-download
make -C src
~~~

Add to Path
~~~
cd fastsynth/lib/cbmc/src/cbmc
export PATH=$PATH:$(pwd)
~~~

Building Fastsynth
~~~
cd fastsynth/src
make
~~~

Add to Path
~~~
cd fastsynth/src/fastsynth
export PATH=$PATH:$(pwd)
~~~

Check fastsynth installation
~~~
fastsynth ./aux_files/simplify_event.sl
fastsynth ./aux_files/gen_event_update.sl
~~~

Python Modules
~~~
dnf install graphviz graphviz-devel pkg-config python3-devel redhat-rpm-config
pip3 install numpy pygraphviz transitions termcolor
~~~


#Linux 

Install Basic Requirements
~~~
apt-get install build-essential
apt-get install g++ gcc flex bison make git libwww-perl patch
~~~

Install Tool Dependencies
~~~
apt-get install python3 cvc4 cbmc z3
~~~

Cloning Fastsynth
~~~
git clone https://github.com/kroening/fastsynth.git
cd fastsynth
git reset --hard b8841e05ef97a35d28fb097fa0e19cc998021997
git submodule init
git submodule update
~~~

Building CBMC
~~~
cd fastsynth/lib/cbmc
make -C src minisat2-download
make -C src
~~~

Building Fastsynth
~~~
cd fastsynth/src
make
~~~

Add to Path
~~~
cd fastsynth/src/fastsynth
export PATH=$PATH:$(pwd)
~~~

Check fastsynth installation
~~~
fastsynth ./aux_files/simplify_event.sl
fastsynth ./aux_files/gen_event_update.sl
~~~

Python Modules
~~~
apt-get install graphviz libgraphviz-dev pkg-config python3-pip python3-setuptools
pip3 install numpy pygraphviz transitions termcolor
~~~


#MacOS

Install Tool Dependencies
~~~
brew install python3
brew tap cvc4/cvc4
brew install cvc4/cvc4/cvc4
~~~

Python Modules
~~~
brew install graphviz
pip3 install pygraphviz --install-option="--include-path=/usr/local/Cellar/graphviz/2.44.0/include/graphviz" --install-option="--library-path=/usr/local/Cellar/graphviz/2.44.0/lib"
pip3 install numpy transitions termcolor
~~~

Install Basic Requirements
Install Xcode 10.x


Cloning Fastsynth
~~~
git clone https://github.com/kroening/fastsynth.git
cd fastsynth
git reset --hard b8841e05ef97a35d28fb097fa0e19cc998021997
git submodule init
git submodule update
~~~

Building CBMC
~~~
cd fastsynth/lib/cbmc
make -C src minisat2-download
make -C src
~~~

Add to Path
~~~
cd fastsynth/lib/cbmc/src/cbmc
export PATH=$PATH:$(pwd)
~~~

Building Fastsynth
~~~
cd fastsynth/src
make
~~~

Add to Path
~~~
cd fastsynth/src/fastsynth
export PATH=$PATH:$(pwd)
~~~

Install Tool Dependencies
~~~
brew install z3
~~~

Check fastsynth installation
~~~
fastsynth ./aux_files/simplify_event.sl
fastsynth ./aux_files/gen_event_update.sl
~~~

