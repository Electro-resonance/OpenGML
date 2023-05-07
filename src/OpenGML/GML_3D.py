# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Martin Timms
# Created Date: 17th April 2023
# License: BSD-3-Clause License
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: 3D variant of OpenGML providing functions to create 3D geometry
# =============================================================================

import numpy as np
from GML import *
from polytopic_geometry import basic_vertices_to_edge_sequence
from polytopic_geometry import vertices_to_edge_sequence

class GML_3D(GML_2D):  # , NodeMixin):  # Add Node feature
    """
    The 3D instance of a GML nested tree of oscillators
    """

    def __init__(self, name, diameter, colour, freq, phase, area=None, parent=None, child=None, mode3D=True):
        super(GML_3D, self).__init__(name, diameter, colour, freq, phase, area=area, parent=parent, child=child, mode3D=True)


    def set_singularity_parameters(self,freq,phase):
        """
        3D variant of setting parameters for a sigularity
        :param freq:
        :param phase:
        :return:
        """
        if (freq[0] == 0 and freq[1] == 0):
            self.bindu = True
            freq[0] = 0.0005
            freq[1] = 0.0005
        else:
            self.bindu = False
        for dimension in range(0, 2):
            self.freq[dimension] = 100 / freq[dimension] + 0.1
            self.orbit_radius[dimension] = abs(freq[dimension])
            self.phase[dimension] = phase[dimension]
            self.start_phase[dimension] = phase[dimension]
            self.cursor_phase[dimension] = phase[dimension]

    def set_freq(self, freq):
        """
        3D variant of adding frequencies
        :param freq:
        :return:
        """
        for dimension in range(0, 2):
            self.freq[dimension] = (100) / freq[dimension] + 0.1
            self.orbit_radius[dimension] = abs(freq[dimension])


    def calc_mypos(self):
        """
        Sum the positions dependent on phases to calculate
        the position of this singularity
        """
        if (self.is_spiral == True):
            return super.calc_mypos() #Use 2D calclulation for spirals
        #self.pos = [self.orbit_radius[0]*trig.fast_cos_deg(
        #   self.phase[0]), self.orbit_radius[0]*trig.fast_sin_deg(self.phase[0]),0]
        sin_theta = trig.fast_sin_deg(-self.phase[0])
        cos_theta = trig.fast_cos_deg(self.phase[0])
        sin_phi = trig.fast_sin_deg(self.phase[1])
        cos_phi = trig.fast_cos_deg(self.phase[1])
        x = self.orbit_radius[0] * sin_theta * cos_phi
        y = self.orbit_radius[0] * sin_theta * sin_phi
        z = self.orbit_radius[0] * cos_theta
        #print(x,y,z,self.phase[0],self.phase[1])
        self.pos = [z,x,y]


        if(self.parent == None):
            self.mypos = [GMLBaseClass.screen_width
                          / 2, GMLBaseClass.screen_height/2,0]
        else:
            self.mypos = self.parent.mypos
        self.mypos = [self.mypos[0]+self.pos[0], self.mypos[1]+self.pos[1], self.mypos[2]+self.pos[2]]

    def add_spherical_coords(self,name, coords, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[0,0]):
        """
        Add a list of spherical points to a sphere to define vertices of a 3D shape
        :param name:
        :param coords:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :return:
        """
        nodes=[]
        i=0
        for [phi,omega] in coords:
            node = GML_3D(name+str(i),diameter=diameter, colour=colour, freq=freq,
                          phase=[omega / math.pi * 180 + offset_angle[0], phi / math.pi * 180 + offset_angle[1]], child=None, parent=self)
            nodes.append(node)
            i+=1
        if(self.edges is not None):
            self.preserve_edges=True
        else:
            self.edges=vertices_to_edge_sequence(coords)
        return nodes

    def add_cartesian_coords(self, name, coords, diameter=1, freq=[1, 1], colour=[255, 255, 255], offset_angle=[0, 0],
                             rotation_matrix=np.array([[1,0,0,0],[1,0,0,0]])):
        """
        Add a list of cartesian points to a sphere to define vertices of a 3D shape
        :param name:
        :param coords:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :param rotation_matrix:
        :return:
        """
        nodes = []
        new_freq = [0,0]
        i = 0
        for x, y, z in coords:
            phi = math.atan2(y, x)
            omega = math.atan2(math.sqrt(x ** 2 + y ** 2), z)
            new_freq[0] = freq[0] * rotation_matrix[0,0] + \
                          freq[0] * (rotation_matrix[0,1] * x) + freq[0] * (rotation_matrix[0,2] * y) + freq[0] * (rotation_matrix[0,3] * z)
            new_freq[1] = freq[1] * rotation_matrix[1,0] + \
                          freq[1] * (rotation_matrix[0,1] * x) + freq[1] * (rotation_matrix[0,2] * y) + freq[1] * (rotation_matrix[0,3] * z)
            node = GML_3D(name + str(i), diameter=diameter, colour=colour, freq=new_freq,
                          phase=[omega / math.pi * 180 + offset_angle[0], phi / math.pi * 180 + offset_angle[1]], child=None, parent=self)
            nodes.append(node)
            i += 1
        if(self.edges is not None):
            self.preserve_edges=True
        else:
            self.edges=vertices_to_edge_sequence(coords)
        return nodes

    def add_polygon(self, name, sides, offset_angle, diameter, freq, colour, levels=1, freq_factor=1.0, polygon_factor=0, rotation_factor=0, crystal=False, colour_change=False):
        """
        Add an n sided polygon to the current node (3D version)
        If levels is provided, a set of nested polygon is added.
        Optional parameters:
        => frequency_factor is a multiplier on the circle size for each nest.
        => polygon_factor is an integer increment or decrement of the number of
        side on each nest.
        => rotation_factor is an integer describing an increment or decrement of
        the number of sides as the shape is rotated.
        """
        node = None
        nodes = []
        angle=offset_angle
        levels -= 1
        rotation_adj = 0
        if(sides <= 0):
            sides = 0
            ang_inc = 0
        else:
            angle_incr = (360/sides)
        for vertex in range(sides):
            node = GML_3D(name+str(levels)+"_"+str(vertex+1),
                          diameter, colour, freq, angle, None, parent=self)
            if(colour_change):
                colour = subtractColours(colour, [-11, -50, -30], 60)
            if(levels > 0):
                if(crystal == True):
                    node.add_polygon(name, sides+polygon_factor+rotation_adj,
                                     offset_angle, diameter, freq*freq_factor, colour, levels)
                else:
                    node.add_polygon(name, sides+polygon_factor+rotation_adj, offset_angle, diameter, freq
                                     * freq_factor, colour, levels, freq_factor, polygon_factor, rotation_factor, crystal)
            angle[0] += angle_incr
            #angle[1] += angle_incr
            rotation_adj += rotation_factor
            nodes.append(node)
        if(len(nodes) > 0):
            return nodes
        else:
            return self

    def add_sphere(self, name, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[1,1], rotation_matrix=np.array([[1,0,0,0],[1,0,0,0]])):
        """
        Add singularity points to the current circle
        """
        sphere_coords=[(1,0,0)]
        return self.add_cartesian_coords(name=name, coords=sphere_coords, diameter=diameter, freq=freq, colour=colour, offset_angle=offset_angle, rotation_matrix=rotation_matrix)

    #https://polytope.miraheze.org/wiki/Tetrahedron
    def add_tetrahedron(self,name, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[0,0], rotation_matrix=np.array([[1,0,0,0],[1,0,0,0]]) ):
        """
        Add vertices for a tetrahedron onto a sphere
        :param name:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :param rotation_matrix:
        :return:
        """
        tetrahedron_coords = [
            (+1 / 2, -math.sqrt(3) / 6, math.sqrt(2) / 4),
            (-1 / 2, -math.sqrt(3) / 6, math.sqrt(2) / 4),
            (0, math.sqrt(3) / 3, -math.sqrt(6) / 12),
            (0, 0, math.sqrt(6) / 4),
            ]

        self.edges = [
            [(0, 1), (1, 2), (2, 0)],  # Face with vertices 0, 1 and 2
            [(0, 1), (1, 3), (3, 0)],  # Face with vertices 0, 1 and 3
            [(0, 2), (2, 3), (3, 0)],  # Face with vertices 0, 2 and 3
            [(1, 2), (2, 3), (3, 1)]  # Face with vertices 1 ,2 and 3
        ]
        return self.add_cartesian_coords(name, tetrahedron_coords , diameter=diameter, freq=freq, colour=colour, offset_angle=offset_angle, rotation_matrix=rotation_matrix)


    #See: https://netlib.org/polyhedra/
    def add_cube(self,name, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[0,0], rotation_matrix=np.array([[1,0,0,0],[1,0,0,0]]) ):
        """
        Add vertices for a cube onto a sphere
        :param name:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :param rotation_matrix:
        :return:
        """
        cube_coords = [
            (-1, -1, -1), #0
            (-1, -1, +1), #1
            (-1, +1, -1), #2
            (-1, +1, +1), #3
            (+1, -1, -1), #4
            (+1, -1, +1), #5
            (+1, +1, -1), #6
            (+1, +1, +1), #7
            ]

        self.edges = [
            [(0, 1), (1, 3), (3, 2), (2, 0)],  # Front face
            [(4, 5), (5, 7), (7, 6), (6, 4)],  # Back face
            [(0, 4), (4, 6), (6, 2), (2, 0)],  # Left face
            [(5, 7), (7, 3), (3, 1), (1, 5)],  # Right face
            [(0, 4), (4, 5), (5, 1), (1, 0)],  # Bottom face
            [(2, 6), (6, 7), (7, 3), (3, 2)]  # Top face
        ]
        return self.add_cartesian_coords(name, cube_coords , diameter=diameter, freq=freq, colour=colour, offset_angle=offset_angle, rotation_matrix=rotation_matrix)

    def add_pyramid(self,name, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[0,0], rotation_matrix=np.array([[1,0,0,0],[1,0,0,0]]) ):
        """
        Add vertices for a pyramid onto a sphere
        :param name:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :param rotation_matrix:
        :return:
        """
        pyramid_coords = [
            (-1, -1, -1), #0
            (-1, +1, -1), #1
            (+1, +1, -1), #2
            (+1, -1, -1), #3
            (0, 0, 1) #4
            ]

        self.edges = [
            [(0, 1), (1, 2), (2, 3), (3, 0)],  # Bottom face
            [(0, 1), (1, 4), (4, 0)],
            [(0, 3), (3, 4), (4, 0)],
            [(2, 1), (1, 4), (4, 2)],
            [(2, 3), (3, 4), (4, 2)]
        ]
        return self.add_cartesian_coords(name, pyramid_coords , diameter=diameter, freq=freq, colour=colour, offset_angle=offset_angle, rotation_matrix=rotation_matrix)


    def add_octohedron(self,name, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[0,0], rotation_matrix=np.array([[1,0,0,0],[1,0,0,0]]) ):
        """
        Add vertices for a octohedron onto a sphere
        :param name:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :param rotation_matrix:
        :return:
        """
        octohedron_coords = [
            (0, 0, +1), #0
            (-1, 0, 0), #1
            (0, +1, 0), #2
            (+1, 0, 0), #3
            (0, -1, 0), #4
            (0, 0, -1), #5
            ]

        self.edges = [
            [(0, 1),(1, 2),(2,0)],
            [(0, 2),(2, 3),(3,0)],
            [(0, 3),(3, 4),(4,0)],
            [(0, 4),(4, 1),(1,0)],
            [(5, 1),(1, 2),(2,5)],
            [(5, 2),(2, 3),(3,5)],
            [(5, 3),(3, 4),(4,5)],
            [(5, 4),(4, 1),(1,5)]
        ]

        return self.add_cartesian_coords(name, octohedron_coords , diameter=diameter, freq=freq, colour=colour, offset_angle=offset_angle, rotation_matrix=rotation_matrix)

    #https://polytope.miraheze.org/wiki/Dodecahedron
    def add_dodecahedron(self,name, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[0,0], rotation_matrix=np.array([[1,0,0,0],[1,0,0,0]]) ):
        """
        Add vertices for a dodecahedron onto a sphere
        :param name:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :param rotation_matrix:
        :return:
        """
        dodecahedron_coords = [
            (-(1 + math.sqrt(5)) / 4, -(1 + math.sqrt(5)) / 4, -(1 + math.sqrt(5)) / 4),
            (-(1 + math.sqrt(5)) / 4, -(1 + math.sqrt(5)) / 4, +(1 + math.sqrt(5)) / 4),
            (-(1 + math.sqrt(5)) / 4, +(1 + math.sqrt(5)) / 4, -(1 + math.sqrt(5)) / 4),
            (-(1 + math.sqrt(5)) / 4, +(1 + math.sqrt(5)) / 4, +(1 + math.sqrt(5)) / 4),
            (+(1 + math.sqrt(5)) / 4, -(1 + math.sqrt(5)) / 4, -(1 + math.sqrt(5)) / 4),
            (+(1 + math.sqrt(5)) / 4, -(1 + math.sqrt(5)) / 4, +(1 + math.sqrt(5)) / 4),
            (+(1 + math.sqrt(5)) / 4, +(1 + math.sqrt(5)) / 4, -(1 + math.sqrt(5)) / 4),
            (+(1 + math.sqrt(5)) / 4, +(1 + math.sqrt(5)) / 4, +(1 + math.sqrt(5)) / 4),
            (-(3 + math.sqrt(5)) / 4, -(1 /2), 0),
            (-(3 + math.sqrt(5)) / 4, +(1 / 2), 0),
            (+(3 + math.sqrt(5)) / 4, -(1 / 2), 0),
            (+(3 + math.sqrt(5)) / 4, +(1 / 2), 0)
        ]
        # self.edges = [
        #     [(0, 8), (8, 4), (4, 10), (10, 2),(2,0)],  # face 0-8-4-10-2
        #     [(0, 2), (2, 6), (6, 11), (11, 3),(3,0)],  # face 0-2-6-11-3
        #     [(0, 3), (3, 9), (9, 1), (1, 8),(8,0)],  # face 0-3-9-1-8
        #     [(1, 9), (9, 3), (3, 11), (11, 7),(7,1)],  # face 1-9-3-11-7
        #     [(1, 7), (7, 5), (5, 10), (10, 8),(8,1)],  # face 1-7-5-10-8
        #     [(2, 10), (10, 5), (5, 7), (7, 6),(6,2)],  # face 2-10-5-7-6
        #     [(3, 11), (11, 6), (6, 7), (7, 9),(9,3)],  # face 3-11-6-7-9
        #     [(4, 8), (8, 1), (1, 5), (5, 10),(10,4)],  # face 4-8-1-5-10
        #     [(4, 5), (5, 6), (6, 2), (2, 10),(10,4)],  # face 4-5-6-2-10
        #     [(0, 9), (9, 6), (6, 7), (7, 11), (11, 3)],  # face
        #     [(0, 8), (8, 11), (11, 6), (6, 9), (9, 3)],  # face
        #     [(0, 2), (2, 10), (10, 11), (11, 7), (7, 3)]  # face
        # ]
        return self.add_cartesian_coords(name, dodecahedron_coords , diameter=diameter, freq=freq, colour=colour, offset_angle=offset_angle, rotation_matrix=rotation_matrix)

    #https://math.stackexchange.com/questions/441327/coordinates-of-icosahedron-vertices-with-variable-radius
    #https://www.classes.cs.uchicago.edu/archive/2003/fall/23700/docs/handout-04.pdf
    def add_icosahedron(self,name, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[0,0], rotation_matrix=np.array([[1,0,0,0],[1,0,0,0]]) ):
        """
        Add vertices for a icosahedron onto a sphere
        :param name:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :param rotation_matrix:
        :return:
        """
        phi = (1 + math.sqrt(5)) / 2
        mult= 1/(math.sqrt(1+phi*phi))
        coords = [
            (+phi, +1, 0),
            (-phi, +1, 0),
            (+phi, -1, 0),
            (-phi, -1, 0),
            (+1, 0, +phi),
            (+1, 0, -phi),
            (-1, 0, +phi),
            (-1, 0, -phi),
            (0, +phi,+1),
            (0, -phi,+1),
            (0, +phi,-1),
            (0, -phi,-1)
        ]

        icosahedron_coords=[]
        for coord in coords:
            icosahedron_coords.append([coord[0]*mult,coord[1]*mult,coord[2]*mult])


        self.edges = [
            [(0, 8),(8, 4),(4,0)],
            [(0, 5),(5, 10),(10,0)],
            [(2, 4),(4, 9),(9,2)],
            [(2, 11),(11, 5),(5,2)],
            [(1, 6),(6, 8),(8,1)],
            [(1, 10),(10, 7),(7,1)],
            [(3, 9),(9, 6),(6,3)],
            [(3, 7), (7, 11), (11, 3)],
            [(0, 10),(10, 8),(8,0)],
            [(1, 8),(8, 10),(10,1)],
            [(2, 9),(9, 11),(11,2)],
            [(3, 9),(9, 11),(11,3)],
            [(4, 2),(2, 0),(0,4)],
            [(5, 0),(0, 2),(2,5)],
            [(6, 1),(1, 3),(3,6)],
            [(7, 3),(3, 1),(1,7)],
            [(8, 6),(6, 4),(4,8)],
            [(9, 4),(4, 6),(6,9)],
            [(10, 5),(5, 7),(7,10)],
            [(11, 7),(7, 5),(5,11)]
        ]
        return self.add_cartesian_coords(name, icosahedron_coords , diameter=diameter, freq=freq, colour=colour, offset_angle=offset_angle, rotation_matrix=rotation_matrix)

    def add_fibonaaci_sphere(self,name, samples=10, diameter=1, freq=[1,1], colour=[255,255,255], offset_angle=[0,0], swap_axis=False,spread_factor=1):
        """
        See: https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
        :param name:
        :param samples:
        :param diameter:
        :param freq:
        :param colour:
        :param offset_angle:
        :param swap_axis:
        :return:
        """
        nodes=[]
        phi = np.pi * (np.sqrt(5.) - 1.)  # golden angle in radians
        for i in range(samples):
            y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
            radius = math.sqrt(1 - y * y)  # radius at y
            theta = phi * i  # golden angle increment
            #latitude=(np.pi/2) - math.atan2(y,radius)
            latitude = np.arccos(y)*spread_factor
            phase= [np.mod(theta/np.pi*180 + offset_angle[0],360),latitude/np.pi*180 +offset_angle[1]]
            if(swap_axis==True):
                temp_phase=phase
                phase=[temp_phase[1],temp_phase[0]]
            #print(phase)
            node = GML_3D(name+str(i),diameter, colour, freq, phase, None, parent=self)
            nodes.append(node)
        if (len(nodes) > 0):
            return nodes

    def gml_line_plot(self, limit, match_frequency=True, fuzzy_match=False, depth=0, line_width=1.0, stipple=False, polygons=False, plot_mode=0):
        """
        Function to plot lines from centre point to the phase singularities.
        """
        quantise_freq = 2
        depth += 1

        gml_child_dictionary = {}
        gml_freq_dictionary = {}
        limit -= 1
        child_count = 0
        if(limit > 0):
            if(len(self.children1) > 0):
                for child_node in self.children1:
                    if (child_node is not None):
                        phase = child_node.start_phase[0]+0.001*child_count
                        gml_child_dictionary[phase] = child_node
                        child_count += 1
                sorted_children = sorted(
                    gml_child_dictionary.items(), key=lambda x: x[0])
                #print("Count:",child_count,"Sorted:",sorted_children)

                start_pos = None
                freq_list = []
                #positions=[]
                for child_node in sorted_children:
                    if (child_node[1] != None):
                        pos = child_node[1].mypos
                        if(match_frequency == True):
                            freq = child_node[1].freq[0]
                        else:
                            freq = 1
                        if(fuzzy_match):
                            closest_freq = self.closest_value(freq_list, freq)
                            if(abs(closest_freq-freq) > quantise_freq):
                                freq_list.append(freq)
                                if freq not in gml_freq_dictionary:
                                    gml_freq_dictionary[freq] = []
                            else:
                                freq = closest_freq
                                #print("matched")
                            #print(freq,closest_freq)
                        if (not freq in gml_freq_dictionary):
                            gml_freq_dictionary[freq] = []
                        gml_freq_dictionary[freq].extend((pos[0], pos[1], pos[2]))

                #print(gml_freq_dictionary.keys)

                for freq_key in gml_freq_dictionary:
                    #Append the start position to the end to complete a polygon
                    start_pos = gml_freq_dictionary[freq_key]
                    gml_freq_dictionary[freq_key].extend(
                        (start_pos[0], start_pos[1], start_pos[2]))

                    #Check for singularities
                    if(len(gml_freq_dictionary[freq_key]) == 4):
                        gml_freq_dictionary[freq_key].extend(
                            (self.mypos[0], self.mypos[1], self.mypos[2]))

                #for freq in gml_freq_dictionary.keys()
                #print(gml_freq_dictionary)

                if (self.preserve_edges==True):
                    plot_mode=2 #Use edges provided for polytope
                for freq_key in gml_freq_dictionary:
                        self.graphics_helper.plot_lines_3D(gml_freq_dictionary[freq_key], [
                               0.8, 0.2+depth/10, 0.8], 0.9, line_width=line_width, stipple=stipple,polygons=polygons,edge_sequence=self.edges,plot_mode=plot_mode)

                for child_node in self.children1:
                    if (child_node != None):
                        child_node.gml_line_plot(
                            limit, match_frequency, fuzzy_match, depth,
                            line_width, stipple, polygons)
        return

    def increment_phase(self):
        for dims in range(0, 2):
            if (GMLBaseClass.reverse == True):
                self.phase[dims] -= self.freq[dims] * GMLBaseClass.oscillator_speed * self.oscillator_speed_node
            else:
                self.phase[dims] += self.freq[dims] * GMLBaseClass.oscillator_speed * self.oscillator_speed_node
            if (self.phase[dims] > 360):
                self.phase[dims] -= 360
            elif (self.phase[dims] < -360):
                self.phase[dims] += 360



def create_bindu_3D(reset_count=True):
    """
    Create the Bindu point at the centre and top of the
    GML tree
    """
    parent_node = None
    bindu_node = GML_3D(
        'Bindu', 0.001, [255, 255, 255], [0,0], [0,0], None, parent=parent_node, mode3D=True)
    if(reset_count == True):
        bindu_node.reset_osc_count()
        GMLBaseClass.osc_count += 1
    return bindu_node