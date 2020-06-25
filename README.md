# Trace2Model
A framework to learn system models from system execution traces. <br/>
Paper: https://arxiv.org/abs/2001.05230

## Usage
`python3 <module_file_name> [args]`<br/>
Use the `-h` option to see module arguments.

Modules available:
1. Incremental NFA learning: `incr.py`
2. DFA learning: `dfa.py`
3. Synthesize expressions that will serve as transition conditions for next event: `syn_next_event.py`
4. Synthesize expressions that will serve as transition predicates for data update across transitions: `syn_event_update.py`

For the synthesis modules 3 and 4, a new trace file `<input_filename>_events.txt` is created with a sequence of transition predicates. Use this as input to the model learning modules 1 and 2.

Use the `-h` option to see module arguments. You can use `run.py` to run a set of benchmarks already present in the tool. See the `benchmarks` folder.

## Tool Dependencies
You'll need the following tools installed (installation instructions for Fedora 29, Ubuntu 18.04 and MacOS 10.15 are provided below):
1. `CVC4 v1.6`: https://cvc4.github.io/downloads.html
2. `CBMC v5.10`: https://www.cprover.org/cbmc/
3. `Fastsynth` : https://github.com/kroening/fastsynth
4. `z3 v4.7.1` : https://github.com/Z3Prover/z3

## Benchmarks
There are a few trace files already provided to play around with the tool in the `benchmarks` folder
1. `dfa_bench` : benchmarks for non-incremental DFA learning
2. `incr_bench` : benchmarks for incremental NFA learning
3. `syn_bench` : benchmarks for predicate synthesis

## Setup Instructions

### Fedora (tested for Fedora 29)

1. Install Basic Requirements
~~~
  dnf groupinstall "Development Tools"
  dnf install kernel-devel kernel-headers
  dnf install gcc gcc-c++ flex bison perl-libwww-perl patch git
~~~

2. Install Tool Dependencies
~~~
  yum install python3
  yum install cvc4
  yum install z3
~~~

Building Fastsynth
~~~
  git clone https://github.com/kroening/fastsynth.git
  cd fastsynth
  git reset --hard b8841e05ef97a35d28fb097fa0e19cc998021997
  git submodule init
  git submodule update
  cd lib/cbmc
  make -C src minisat2-download
  make -C src
  export PATH=$PATH:$(pwd)/src/cbmc
  cd ../../src
  make
  cd fastsynth
  export PATH=$PATH:$(pwd)
~~~

3. Python Modules
~~~
  dnf install graphviz graphviz-devel pkg-config python3-devel redhat-rpm-config
  pip3 install numpy pygraphviz transitions termcolor
~~~

4. Clone the repository `Trace2Model`<br/>
Check Fastsynth installation : Move to `Trace2Model` folder and run
~~~
  cd Trace2Model
  fastsynth ./aux_files/simplify_event.sl
  fastsynth ./aux_files/gen_event_update.sl
~~~


### Linux (tested on Ubuntu 18.04)

1. Install Basic Requirements
~~~
  apt-get install build-essential
  apt-get install g++ gcc flex bison make git libwww-perl patch
~~~

2. Install Tool Dependencies
~~~
  apt-get install python3 cvc4 cbmc z3
~~~

Building Fastsynth
~~~
  git clone https://github.com/kroening/fastsynth.git
  cd fastsynth
  git reset --hard b8841e05ef97a35d28fb097fa0e19cc998021997
  git submodule init
  git submodule update
  cd lib/cbmc
  make -C src minisat2-download
  make -C src
  cd ../../src
  make
  cd fastsynth
  export PATH=$PATH:$(pwd)
~~~

3. Python Modules
~~~
  apt-get install graphviz libgraphviz-dev pkg-config python3-pip python3-setuptools
  pip3 install numpy pygraphviz transitions termcolor
~~~

4. Clone the repository `Trace2Model`<br/>
Check Fastsynth installation : Move to `Trace2Model` folder and run
~~~
  cd Trace2Model
  fastsynth ./aux_files/simplify_event.sl
  fastsynth ./aux_files/gen_event_update.sl
~~~




### MacOS (tested on MacOS 10.15)

1. Python Modules
~~~
  brew install python3
  brew install graphviz
  pip3 install numpy transitions termcolor
~~~
  Include graphviz PATH for pygraphviz installation as shown below:
~~~
  pip3 install pygraphviz --install-option="--include-path=/usr/local/Cellar/graphviz/2.44.0/include/graphviz" --install-option="--library-path=/usr/local/Cellar/graphviz/2.44.0/lib"
~~~

2. Install Tool Dependencies
~~~
  brew tap cvc4/cvc4
  brew install cvc4/cvc4/cvc4
  brew install z3
~~~

  Building Fastsynth<br/>
  Install Xcode 10.x for Fastsynth build
~~~
  git clone https://github.com/kroening/fastsynth.git
  cd fastsynth
  git reset --hard b8841e05ef97a35d28fb097fa0e19cc998021997
  git submodule init
  git submodule update
  cd lib/cbmc
  make -C src minisat2-download
  make -C src
  export PATH=$PATH:$(pwd)/src/cbmc
  cd ../../src
  make
  cd fastsynth
  export PATH=$PATH:$(pwd)
~~~


3. Clone the repository `Trace2Model`<br/>
  Check Fastsynth installation : Move to `Trace2Model` folder and run
~~~
  cd Trace2Model
  fastsynth ./aux_files/simplify_event.sl
  fastsynth ./aux_files/gen_event_update.sl
~~~

