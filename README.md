# Trace2Model
A framework to learn system models from system execution traces.

## Usage
Modules available:
1. Incremental NFA learning: `incr.py`
2. DFA learning: `dfa.py`
3. Synthesize expressions that will serve as transition conditions for next event: `syn_next_event.py`
4. Synthesize expressions that will serve as transition preducates for data update across transitions: `syn_event_update.py`

For synthesis, a new trace file `<input_filename>_events.txt` is created with transition predicates.

Use the `-h` option to see module arguments. You can use `run.py` to run a benchmarks already present in the tool. See `benchmarks` folder.

## Setup Instructions

### Fedora

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

Building CBMC : change to the CBMC directory `fastsynth/lib/cbmc` and run make
~~~
cd lib/cbmc
make -C src minisat2-download
make -C src
~~~

Add to Path: add `fastsynth/lib/cbmc/src/cbmc` to PATH
~~~
export PATH=$PATH:$(pwd)/src/cbmc
~~~

Building Fastsynth : change to the Fastsynth directory `fastsynth/src` and run make
~~~
cd ../../src
make
~~~

Add to Path : add `fastsynth/src/fastsynth` to PATH
~~~
cd fastsynth
export PATH=$PATH:$(pwd)
~~~

Check Fastsynth installation : Move to the main tool folder `Trace2Model` and run
~~~
fastsynth ./aux_files/simplify_event.sl
fastsynth ./aux_files/gen_event_update.sl
~~~

Python Modules
~~~
dnf install graphviz graphviz-devel pkg-config python3-devel redhat-rpm-config
pip3 install numpy pygraphviz transitions termcolor
~~~


### Linux (tested on Ubuntu 18.04)

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

Building CBMC : change to the CBMC directory `fastsynth/lib/cbmc` and run make
~~~
cd lib/cbmc
make -C src minisat2-download
make -C src
~~~

Building Fastsynth : change to the Fastsynth directory `fastsynth/src` and run make
~~~
cd ../../src
make
~~~

Add to Path : add `fastsynth/src/fastsynth` to PATH
~~~
cd fastsynth
export PATH=$PATH:$(pwd)
~~~

Check Fastsynth installation : Move to the main tool folder `Trace2Model` and run
~~~
fastsynth ./aux_files/simplify_event.sl
fastsynth ./aux_files/gen_event_update.sl
~~~

Python Modules
~~~
apt-get install graphviz libgraphviz-dev pkg-config python3-pip python3-setuptools
pip3 install numpy pygraphviz transitions termcolor
~~~


### MacOS (tested on MacOS 10.15)

Install Tool Dependencies
~~~
brew install python3
brew tap cvc4/cvc4
brew install cvc4/cvc4/cvc4
~~~

Python Modules
~~~
brew install graphviz
~~~
Include graphviz PATH for pygraphviz installation as shown below:
~~~
pip3 install pygraphviz --install-option="--include-path=/usr/local/Cellar/graphviz/2.44.0/include/graphviz" --install-option="--library-path=/usr/local/Cellar/graphviz/2.44.0/lib"
~~~
Install other modules
~~~
pip3 install numpy transitions termcolor
~~~

Install Xcode 10.x for Fastsynth build

Cloning Fastsynth
~~~
git clone https://github.com/kroening/fastsynth.git
cd fastsynth
git reset --hard b8841e05ef97a35d28fb097fa0e19cc998021997
git submodule init
git submodule update
~~~

Building CBMC : change to the CBMC directory `fastsynth/lib/cbmc` and run make
~~~
cd lib/cbmc
make -C src minisat2-download
make -C src
~~~

Add to Path: add `fastsynth/lib/cbmc/src/cbmc` to PATH
~~~
export PATH=$PATH:$(pwd)/src/cbmc
~~~

Building Fastsynth : change to the Fastsynth directory `fastsynth/src` and run make
~~~
cd ../../src
make
~~~

Add to Path : add `fastsynth/src/fastsynth` to PATH
~~~
cd fastsynth
export PATH=$PATH:$(pwd)
~~~

Install Tool Dependencies
~~~
brew install z3
~~~

Check Fastsynth installation : Move to the main tool folder `Trace2Model` and run
~~~
fastsynth ./aux_files/simplify_event.sl
fastsynth ./aux_files/gen_event_update.sl
~~~

