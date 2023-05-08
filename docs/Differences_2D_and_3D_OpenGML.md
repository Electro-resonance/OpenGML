## Differences between 2D and 3D OpenGML

There are subtle differences between OpenGML in 2D and 3D which use completely different graphics environments. OpenGML
is written such that the effect of these differences is minimised to the user. Examples for 2D and 3D OpenGML are very 
similar apart from the applications framework chosen and the type of Bindu used. Here is a summary of the 
underlying differences:

|                                     | OpenGML 2D                     | OpenGML 3D                                 |
|-------------------------------------|--------------------------------|--------------------------------------------|
| Graphics Engine                     | Kivy                           | PyGame plus OpenGL                         |
| Use of blits                        | yes                            | no                                         |
| Use of OpenGL graphics rendering    | no                             | yes                                        |
| Core Functions                      | GML.py                         | GML_3D.py                                  |
| Abstraction Layer                   | GML_App_2D.py                  | GML_APP_3D.py                              |
| Graphics Functions                  | blit_functions.py              | pygame_functions.py                        |
| Class Constructor                   | GML()                          | GML_3D()                                   |
| Applications framework              | GML_App_2D()                   | GML_App_3D()                               |
| Bindu creation method               | create_bindu()                 | create_bindu_3D()                          |
| Runtime callback                    | add_runtime_callback()         | add_runtime_callback()                     |
| Key callback                        | add_key_callback(key_callback) | Not implemented                            |
| 2D shapes                           | yes                            | yes                                        |
| Spiral oscillators                  | yes                            | no                                         |
| Pendulum oscillators                | yes                            | no                                         |
| Linear oscillators                  | yes                            | no                                         |
| 3D polytopes                        | no                             | yes                                        |
| Ability to mix 2D and 3D primitives | no                             | yes                                        |
| Sonification                        | yes                            | Partial implementation (under development) |
| Animation of sonification           | yes                            | no                                         |

