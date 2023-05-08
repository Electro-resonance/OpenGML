# OpenGML Background
### OpenGML.org

OpenGML is an open-source project that originated from collaborations between Martin Timms and Dr Anirban Bandyopadyay. 
Martin had been in discussions with Anirban about resonances within biology since 2014 when Martin worked on a voluntary 
project to measure RF emissions from humans. Dr Anirban Bandyopadyay's work on Microtubules and work with Stuart Hameroff 
on the experimental mechanisms within biology for consciousness to form. This correspondence continued as Martin was 
asked to work on a project to development a data acquisition system for plant electrophysiology with the founders of 
Vivent Sarl https://vivent.ch/, which included months of testing and analysis of small electrophysiology signals recorded 
from plants. These signals revealed complex circadian patterns including higher frequency signalling. This work on 
electrophysiology led Martin to discover the applicability of Anirban's work on Microtubules in interfacing with many 
areas of biology. Martin's collaboration continued with Anirban and they met at The Science of Consciousness conferences 
at TSC 2017 in San Diego and TSC 2018 in Tuscon. At both conferences work was done on devices relating to nanoAmpere and 
nanoVolt measurement for reducing the cost of instrumentation to measure signalling within Microtubules.
From 2017 Martin Timms has been an engineering advisor to IIoIR, Shimla, India: https://www.iioir.org/

### Nanobrains, Organic Gel and Dodecahedron Quantum Based Computers

In January 2021, Martin was invited by Anirban to be one of the founders of NanoBrainTech https://nanobraintech.com/ a 
technology transfer office (TTO) to assist in the development and commercialisation of technologies relating to 
Dr Anirban's dicoveries and his work on Nanobrains, Organic Gel based Computers and Dodecahedron Quantum Based Computers.
To bridge the gap between this new technology and the existing scientific community, it was decided to develop
open source tools to allow for experimentation with the concepts of GML and allow experimentation with some of the 
use cases such as sonification. The result of this open source work (OpenGML) will also be used in future projects as
interfaces with biology and with the new Organic Gel and Dodecahedron Quantum Based Computers as the technology evolves.
The first step to this open source work was to taking the Martin's GML code and translate this to Kivy for use on an 
Android app. The resulting work is the culmination of daily correspondences between Martin and Anirban with incremental 
improvements based on the feedback. In many cases this has been a learning process as the process of student-centred 
learning was followed whereby all is not revealed, but instead it is the student that has to learn and by following this
process there is a greater propensity for development of new ideas and approaches.
Ongoing work has included extending the basics of OpenGML to video feeds and interfacing with the outputs of Organic Gel
based artificial brains which results in new interfaces with what is probably the most powerful artificial organic 
computers on the planet.

### Initial GML experiments with PyGame

The code leading towards OpenGML was initially written using PyGame in the days leading to 9th February 2022 using 
OpenGL for graphics for both 2D and 3D. Some initial demos looked 3D, but were in fact 2D using 64, 364 and 1093 
oscillators to run in parallel. By 16th February 2022 a true 3D implementation was able to generate oscillators on a
3D bloch sphere model.

### Sonification

Sonification was first added on 24th February 2022 initially using an external software MIDI interface to control
notes on Apple's GarageBand. Code was written to map 2D images onto GML by abstraction of identified geometry. The 
resulting structures had sonification applied by associating the frequency of oscillators and positions of phase 
singularities via the control of MIDI notes.

### Kivy development

A new version of the software was required to run as an app on Android , which required adapting PyGame to Kivy. 
Although Kivy has the disadvantage of using OpenGL under the hood, its 2D graphics engine is designed specifically to 
work in the 2D plane. Initially, Kivy was quite slow at rendering graphics in real-time, as the 2D graphics engine 
required the CPU to redraw shapes each time they were called, rather than offloading to the GPU graphics processor.

To overcome this issue, Kivy relies heavily on the use of "blits" for game development. These "blits" are similar to 
the "sprites" used on 8-bit computers, but they make full use of the GPU via OpenGL to speed up movement, replication, 
rotations, changes in color, and scaling. To speed up OpenGML, "blits" are created using Kivy's 2D graphics primitives 
and then cached. Any reference to the shape or similar shape then uses the cached image, which is an ultra-fast process 
that takes place on the GPU graphics card.

For example, circles in 2D OpenGML are created using a square "blit" onto which a circle is plotted. Most of the "blit" 
is populated with a transparent color so that only the circle is displayed and can be layered many times with other 
circles. Similar use of "blits" is used for other OpenGML 2D shapes such as spirals. Overall, the use of "blits" in 
Kivy has greatly improved the speed and efficiency of OpenGML on all platforms.


### Sonification within OpenGML as developed on the Kivy based platform
The sonification of GML was further developed by the inclusion and use of FluidSynth library. This library is able to 
load ".sf2" format soundfonts including GM libraries. Once a GM library is loaded multiple instruments can be played as
virtual midi instruments. FluidSynth allows stereo panning of sounds and up to 64 concurrent notes. OpenGML makes full 
use of the panning and channel capability by associating many oscillators with many notes and voices automatically panned
into different positions in the stereo field.
Initially when sonifcation was developed the notes were selected using the standard 127 MIDI notes ranging in pitch from
A0 to G9. The midi tuning standard uses equal temperament tuning with 440Hz tuning. When Anirban first hear this, he
did not think it was representative of the GML as the frequencies of the geometries were being quantised to match 
Western musical scales. As well as the standard notes, MIDI and FluidSynth allow pitch bends of +/-2 semitones scaled 
as 8192 values of pitch bend. By combining MIDI notes and pitchbend and using both microtonal scales can be played. 
Various scales where tried including those of Sama Gana scale, Ramamatya scale, Raga scales and scales based on 
pythagorean and fibonacci ratios, however each introduces it's own musical bias. Anirban steered the development to 
using no quantisations of the notes and pitches so that the full microtonal scale can be used and the ratios of notes 
played match exactly the ratios of the geometric circles and their allocated frequencies. By following this approach the 
human ear is presented with the GML as per the geometry displayed with no bias towards any musical scale.

In the playing of notes the pitch is mapped to circumference of the circle which represents a period having a frequency.
The playing of notes is triggered based on the singularity passing a given place on the circle. The graphical "blits" 
generated by Kivy are used for displaying small star shapes used to animate the graphics when sonification is applied. 
The star shapes indicate events occurring during the rotation of a singularity past a given point which is used as the 
trigger for the sound. Within a phase space the events occurring as a singularity passes a point as relating to the 
Orch-OR theory of consciousness has been termed a "Bing" event by Stuart Hameroff and the same naming is used for 
OpenGML sonification.

The Sonification of the Kivy version of OpenGML was developed specifically to allow new forms of communication with
an artifical brain made from nanogel material developed by Dr Anirban Bandyopadhyay. And to the allow interactions 
with the artifical brain with humans using a natural interface. The use of up to 64 polyphony stereo panned sound 
using microtonal pitch allows for vast amounts of musical expression direct to a person from the artifical nanogel 
brain.


### Merging of Kivy with PyGame for 2D and 3D environments
In order to make OpenGML open source, it was necessary to merge two variants of the language that had diverged in their 
use of graphics engines. One variant had used Kivy for 2D, while the other had used PyGame and OpenGL for 3D. Merging 
these two strands required considerable effort to bring together the best aspects of each while preserving backwards 
compatibility with software built on OpenGML. The result was the creation of two classes of GML, one for 2D and one 
for 3D, with the latter class extending the former. The graphics engines were abstracted, allowing OpenGML examples 
for one to be used on the other with minimal modification.

As a result of this merging, nested 2D geometry can now be displayed in 3D, and 3D geometries can include both 3D 
objects such as polytopes and 2D surfaces such as triangles and squares. The code for running OpenGML applications 
has also been abstracted, making it possible to write demos without having to write application layer code.

### Use with ChatGPT
It has been found that by providing copies of the example code, users can quickly learn to program examples in OpenGML. 
Additionally, it has been discovered that large language models (LLMs) such as ChatGPT can be used to discuss new 
features and provide suggestions on how to code and implement those features. However, it should be noted that LLMs are 
not perfect and the user may need to edit and select the code and do their own development.

It is worth experimenting combining elements of OpenGML with ChatGPT and similar LLMs.

### TSC2023 
This work will be presented at The Science of Consciousness Conference in Taormina, Scily: 
https://tsc2023-taormina.it/

The abstract for the relating conference concurrent session to be presented is as follows:

### Abstract
#### C-15 (Wed): Experimental Geometrical Musical Language (GML) Nested Clock
Universes, the Definition of Bindu and the Philosophical Similarities to One That Arises From Simulation
Martin Timms 1,2, Anirban Bandyopadhyay 2,1
1 IIoIR, Shimla, Himachal Pradesh, India. 2 NIMS, Tsukuba, Ibaraki, Japan
#### Categories by Discipline
4.0 Physical and Biological Sciences
#### Primary Topic Area-TSC Taxonomy
[04.05] Emergence, nonlinear dynamics and complexity
#### Abstract
Geometric Musical Language (GML) was first developed by Anirban Bandyopadhyay et al.
(2018) to describe nested periodic clock interactions observed experimentally within
microtubules and protein assemblies. GML is hereby demonstrated to provide the basis of a
universal framework to create simulated n-dimensional universes. Such dynamic nested
clock GML universes can be created as simulations within a GPU-accelerated computing
platform to provide 2D or 3D real-time visualisations, allowing observation of the complex
nested clock architecture interactions. OpenGML demonstrates emergent behaviours
revealing underlying connectivity and provides new methods for computational analysis.
The open source OpenGML software platform developed will allow for collaborative
experimentation. The OpenGML universe can be extended to encode video, images, audio,
or other quantitative based data (such as from sensors) into representations which contain
and reveal detail of the underlying connected geometries and periodicities. GML also allows
projection of higher dimensional structures back into simpler lower dimensional forms, for
example via sonification. In creating a GML universe it quickly becomes immediately
apparent that the universal observation point is very important. This forms what has been
termed the Bindu or centre of the universe and is always the very first point defined when
creating such universes. The Bindu is the point from which all other clocks, geometries and
points are nested. Is the Bindu the ultimate observer of its own universe? The flow of time
in a GML universe applies at all nested clock levels and is exerted as the flow of singularity
points around many clocks. The Bindu being a pure singularity is an exception, and as such
it is exists external to time. Within the GML universe, all clocks and singularity points on
those clocks are a nested feature of Bindu, so the GML universe has inherent connectivity
seeded from the Bindu, a singularity point or ‘One’, a universal consciousness. The
simulated GML universe has rules that parallel with the ideology of pantheism where all in
the universe is inherently connected with the higher instance of itself. The simulated GML
universe is non-material in that all points within the universe are constructed only of
nested singularities with no requirement for matter. In such a universe, flow of information
is inherent by interconnection. The GML universe is fractal. A small observable part will
look self-similar to the whole. All nested levels apply the same connectivity pattern and
rules. It is neither an open universe nor a closed universe, GML defines instead an eternal
interconnected universe. It would be possible for GML to define a layer in the fabric of
reality in a similar way postulated of the quantum world. Is it that such a base layer fabric
of reality, over and above which time and space become emergent layers? The process of
taking an abstract geometric, mathematical, and oscillatory language (GML) applying that
to the experimental creation of simulated computer-generated universes (using OpenGML),
yields insights beyond just mathematics and physics by creating a new framework for
philosophical discussion whilst creating software having application to future AI and bio-interfaces.
#### Keywords
GML, geometry, resonance, clock architecture, simulation, AI, One, Pantheism, Bindu,
Universal Consciousness

## Further Reading
1. Bandyopadhyay, A. (2020). NanoBrain – The Making of an Artificial Brain from a Time Crystal
2. Bandyopadhyay, Anirban. (2021) SOMU theory of consciousness. www.nanobraintech.com https://nanobraintech.com/2021/05/06/somu-theory-of-consciousness/
3. Bandyopadhyay, A.  et al. (2020). US Patent US20200160174 “Universal Geometric-Musical Language For big data processing in an assembly of clocking resonators “
4. Wolfram, S. (2020). A Project To Find The Fundamental Theory of Physics
5. Bandyopadhyay, A. et al. (2017). Fractal Information Theory (FIT)-Derived Geometric Musical Language (GML) for Brain-Inspired Hypercomputing
6. Hameroff, S. Penrose, R. (2014 )Consciousness in the universe: a review of the 'Orch OR' theory. 
7. Wilczek, F. et al. Zakrzewski, J. (2012). Viewpoint: Crystals of Time. physics.aps.org. APS Physics
7. Amelino-Cameliaa, G., Freidelc, L., Kowalski-Glikmanb, J., & Smolinc, L. (2011) The principle of relative locality
8. Strogatz, S. (2004). Sync: The Emerging Science of Spontaneous Order
9. Wolfram, S. (2002). A New Kind of Science
10. Winfree, A. (1986). The Timing of Biological Clocks. 
11. Winfree, A. (1980). The Geometry of Biological Time.
12. M. Narducci, C. Alton Coulter, and Charles M. Bowden (1974). Exact diffusion equation for a model for superradiant emission 
13. F. T. Arecchi, Eric Courtens, Robert Gilmore, and Harry Thomas (1972). Atomic Coherent States in Quantum Optics
14. Feynmann, Venon and Hellwarth (1957). Geometrical Representation of the Schrodinger Equation for Solving Maser Problems
15. Bloch, F. (1946). Nuclear Induction
16. Bose, J.C. (1926). The Nervous Mechanisms of Plants
17. Einstein, A. (1905). On the electrodynamics of moving bodies.
18. Gibbs, J. W. (1903) Principles in Statistical Mechanics
19. Poincare, H (1899) Les me´thodes nouvelles de la me´canique ce´leste 
20. Boltzmann, L (1871), Wien. Ber.63, 679, Vorlesungen über Gastheorie
21. Lissajous, J. A. (1857) Mémoire sur l'étude optique des mouvements vibratoires
22. Tu-Shun (557-640 CE). Avatamsaka Sutra

## WebLinks and Software
1. https://en.wikipedia.org/wiki/MIDI_tuning_standard
2. https://member.keymusician.com/Member/FluidR3_GM/index.html
3. https://www.fluidsynth.org/
3. https://www.pygame.org
4. https://kivy.org/
5. https://chat.openai.com/
