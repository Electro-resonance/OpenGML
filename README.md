# OpenGML
### OpenGML - Open Geometric Music Language
#### OpenGML.org

A language for creating nested geometries based on a mathematical Geometric Musical Language (GML). GML is a language 
originally developed to describe the complex resonances within Microtubules occurring in the form of 
"Triplet of Triplet" resonance bands. GML provides the foundations for constructing simulations of 
"Polyatomic Time Crystals" using 3D Bloch Spheres, for simulating "Self Operating Mathematical Universes" 
(SOMU) and, for development of interfaces between biology and AI.

## Recently added or updated 🆕 ✨
- [The Science of Conference Concurrent Talk by Martin Timms](docs/TSC_Talk)[28th May,2023]
- [The development and history of OpenGML](docs/Development_History.md) [8th May, 2023]
- [The differences between 2D and 3D OpenGML](docs/Differences_2D_and_3D_OpenGML.md) [8th May, 2023]
- [Examples of 2D OpenGML](examples/OpenGML_2D) [7th May, 2023]
- [Examples of 3D OpenGML](examples/OpenGML_3D) [7th May, 2023]
- [Examples demonstrating Phase Coupling](examples/OpenGML_Linkages) [7th May, 2023]
- [Triplet of Triplet Resonance Model](examples/OpenGML_3D/3D_Triplet_of_Triplet.py) [7th May, 2023]
- [Basic Symmetry_Breaking for a 2D SOMU](examples/OpenGML_Linkages/Symmetry_Breaking.py) [15th May, 2023]
- [Balanced Symmetry_Breaking for a 2D SOMU](examples/OpenGML_Linkages/Balanced_Symmetry.py) [16th May, 2023]


## Project Contacts ✨
- [Martin Timms](https://linkedin.com/in/martin-timms-6a135282)
- [Anirban Bandyopadhyay](https://www.linkedin.com/in/anirbanbandyopadhyay)

#/# Highlights ✨
- [Screenshot of Triplet of triplet resonance](screenshots/Triplet_of_Triplet_OpenGML.jpg)
- [Videos of OpenGML](https://www.youtube.com/playlist?list=PLDK0CIWefiIIk_LC1tAPf3LZdCUjGhIK3)
- - [The Science of Conference Concurrent Talk by Martin Timms](docs/TSC_Talk)


#### Academic references for GML:

1. Bandyopadhyay, Anirban. (2019). [Nanobrain: The Making of an Artificial Brain from a Time Crystal.](https://www.taylorfrancis.com/books/mono/10.1201/9780429107771/nanobrain-anirban-bandyopadhyay)
2. Bandyopadhyay, A. et al. (2022). [Polyatomic time crystals of the brain neuron extracted microtubule are projected like a hologram meters away.](https://pubs.aip.org/aip/jap/article/132/19/194401/2837827/Polyatomic-time-crystals-of-the-brain-neuron?s=09) 
3. Bandyopadhyay, A. et al. (2020). [US Patent US20200160174 “Universal Geometric-Musical Language For big data processing in an assembly of clocking resonators “](https://uspto.report/patent/app/20200160174) 
4. Bandyopadhyay, A. et al.  (2018). [Fractal Information Theory (FIT)-Derived Geometric Musical Language (GML) for Brain-Inspired Hypercomputing.](https://link.springer.com/chapter/10.1007/978-981-10-5699-4_33)
5. Bandyopadhyay, Anirban. (2021) [SOMU theory of consciousness.](https://nanobraintech.com/2021/05/06/somu-theory-of-consciousness/)

#### Academic references relating to time crystals and clock based models:

6. Wolfram, S. (2020). [A Project To Find The Fundamental Theory of Physics](https://www.wolfram-media.com/products/a-project-to-find-the-fundamental-theory-of-physics/)
7. Wilczek, F. et al. Zakrzewski, J. (2012). Viewpoint: Crystals of Time. physics.aps.org. APS Physics 
8. Amelino-Cameliaa, G., Freidelc, L., Kowalski-Glikmanb, J., & Smolinc, L. (2011) The principle of relative locality 
9. Strogatz, S. (2004). [Sync: The Emerging Science of Spontaneous Order](https://www.stevenstrogatz.com/books/sync-the-emerging-science-of-spontaneous-order)
10. Wolfram, S. (2002). [A New Kind of Science](https://www.wolframscience.com/nks/)
11. Winfree, A. (1986). [The Timing of Biological Clocks.](https://openlibrary.org/books/OL2722076M/The_timing_of_biological_clocks) 
12. Winfree, A. (1980). [The Geometry of Biological Time.](https://openlibrary.org/works/OL4448379W/The_geometry_of_biological_time?edition=key%3A/books/OL1857963M)

#### Academic references relating to bloch spheres and phase space:
13. Bloch, F. (1946). Nuclear Induction
14. Einstein, A. (1905). On the electrodynamics of moving bodies. 
15. Gibbs, J. W. (1903) Principles in Statistical Mechanics 
16. Poincare, H (1899) Les me´thodes nouvelles de la me´canique ce´leste 
17. Boltzmann, L (1871), Wien. Ber.63, 679, Vorlesungen über Gastheorie 
18. Lissajous, J. A. (1857) Mémoire sur l'étude optique des mouvements vibratoires

### Technical Detail
OpenGML provides two interchangeable frameworks using Kivy for 2D OpenGML and Pygame with OpenGL for 3D OpenGML.
Both frameworks support the addition of sonification using FluidSynth and GM SoundFonts (.sf2) to create stereo panned
soundscapes using atonal frequencies based on the geometry of the OpenGML structures modelled.

### Pre-Requisites
Python 3.9.10

A Kivy environment with following installed into the Kivy python environment):
Under the command line a command such as the follows is needed to activate the Kivy environment before
installing packages. See: https://kivy.org/doc/stable/gettingstarted/installation.html
```python:
source kivy_venv/bin/activate
```

The following packages are required by OpenGML
```python:
pip3 install numpy
pip3 install scikit-image
pip3 install opencv-python
pip3 install pyFluidSynth
pip3 install pyttsx3
pip3 install pygame
```
OpenGML can also be installed under an IDE such as PyCharm which has options to set up Python environments: 
https://www.jetbrains.com/pycharm/


### FluidSynth and GM soundfonts (.sf2)
The (250Mbyte) General Midi (GM) music instrument file:
https://keymusician01.s3.amazonaws.com/FluidR3_GM.zip

The lib files for FluidSynth need to be copied to the same directory as the python code. They can be downloaded from here in the bin folder:
https://github.com/FluidSynth/fluidsynth/releases

### Examples
There are many examples in the following directories of this repository:
```python:
examples/OpenGML_2D
examples/OpenGML_3D
examples/OpenGML_Linkages
```


## Disclaimer
Please be aware that OpenGML applications can cause stroboscopic visual displays. 
If you have any medical conditions especially relating to stroboscopic and/or flashing visual triggers, 
please consult with your doctor before using OpenGML.


