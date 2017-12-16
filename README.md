# The Payne
=====

Artificial Neural-Net compression and fitting of synthetic spectral grids. The code has the following functionality:

* Using PyTorch to train an artificial neural-network on individual pixels in a grid of spectra and/or photometry

* Testing and Validation of a trained ANN to evaluate its precision and calculate the covariance in the predictions

* Fit observed spectra and/or photometry using a trained ANN

The initial algorith framework for The Payne is given in Ting et al. (2016) and Rix et al. (2016). This code follows 
this approach, with additional changes in the fitting and training procedures.

Authors
-------

* **Phillip Cargile** (Harvard)
* **Yuan-Sen Ting** (Carnegie-Princeton-IAS Fellow)

See [Authors](authors.rst) for a full list of contributors to The Payne.

Installation
------
```
cd <install_dir>
git clone https://github.com/pacargile/ThePayne.git
cd ThePayne
python setup.py install (--user)
```

Then in Python
```python
import Payne
```

The Payne is pure python.
See the [tutorial](demo/) for fitting a solar mock with photometric and spectroscopic data.

The user either need to train a new ANN for an observed spectrum and photometry. Or contact <pcargile@cfa.harvard.edu> to get the latest C3K based ANN. 


License
--------

Copyright 2015 the authors. TheCannon is open-source software released under 
the MIT License. See the file ``LICENSE`` for details.


***The Payne is named in honor of Cecilia Payne-Gaposchkin, one of the great scientist of the 20th century and a pioneering in stellar astrophysicist. In the 1920s she derived the cosmic abundance of the elements from stellar spectra, including determining the composition of the Sun, and demonstrated for the first time the chemical homogeneity of the universe. Cecilia Payne-Gaposchkin achieved two Harvard firsts: she became the first female professor, and the first woman to become department chair.***

<https://en.wikipedia.org/wiki/Cecilia_Payne-Gaposchkin>
