##############################################################################
# This software is licensed under a modified MIT license. The MIT license itself
# is unchanged, we have only added an optional beerware clause (based off of
# Poul-Henning Kamp's Beerware license). That is to say, you have the option
# of completely disregarding the beerware clause and using this software under
# the vanilla MIT license if you so wish.
#
# Copyright (c) 2013 Chris Gibson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Optional beerware clause:
# If we happen to meet in person someday and you think this software is worth
# it, you are welcome to buy us a round of beers. This clause is entirely
# optional, and need not be fulfilled for you to fully comply with the terms
# of this license.
##############################################################################

from glm import vec3
import numpy as np


class SubdMesh(object):

    def __init__(self):
        self._vertices = []
        self._quads = []

    # Add a vertex to the mesh
    def addVertex(self, v):
        self._vertices.append(v)
        return len(self._vertices) - 1

    # Add a quad to the mesh
    def addQuad(self, v1, v2, v3, v4):

        for idx in [v1,v2,v3,v4]:
            if idx > len(self._vertices):
                raise ValueError("idx %s is out-of-bounds (> %s)" % (idx,len(self._vertices)))

        self._quads.append([v1, v2, v3, v4])
        return len(self._quads) - 1

    # Return a flat array based on the mesh data
    def toFloatArray(self):
        array = []

        for quad in self._quads:
            for idx in quad:
                v = self._vertices[idx]
                array.extend([v.x, v.y, v.z, 1])

        return np.array(array, dtype=np.float32)

    # Return a cube mesh
    @classmethod
    def buildCube(cls):
        msh = cls()

        # Add the vertices of the cube
        msh.addVertex( vec3(-1, -1, -1) )
        msh.addVertex( vec3(-1, -1,  1) )
        msh.addVertex( vec3( 1, -1,  1) )
        msh.addVertex( vec3( 1, -1, -1) )
        msh.addVertex( vec3(-1,  1, -1) )
        msh.addVertex( vec3(-1,  1,  1) )
        msh.addVertex( vec3( 1,  1,  1) )
        msh.addVertex( vec3( 1,  1, -1) )

        # Generate the faces of the cube
        msh.addQuad(0, 4, 7, 3) # -z face
        msh.addQuad(1, 2, 6, 5) # +z face
        msh.addQuad(0, 1, 5, 4) # -x face
        msh.addQuad(3, 7, 6, 2) # +x face
        msh.addQuad(0, 3, 2, 1) # -y face
        msh.addQuad(4, 5, 6, 7) # +y face

        return msh

    # Return the average of the given indices
    def midpoint(self, *indices):
        mpoint = vec3(0, 0, 0)
        for idx in indices:
            mpoint = mpoint.add(self._vertices[idx])

        return mpoint.div_f(len(indices))

    # Find all faces that contain the given indices
    def quadsContain(self, *indices):
        connected = []

        # For every quad
        for curQuad, quadVerts in enumerate(self._quads, 0):

            # If every indice exists in the quad, add it to our list
            for idx in indices:
                if not idx in quadVerts:
                    break
            else:
                connected.append(curQuad)

        return connected

    # Return any vertices that are connected via edge to the given vertId
    def connectedVerts(self, vertIdx):
        connectedVertIndices = []

        # For every quad in the mesh
        for quadVerts in self._quads:
            polySize = len(quadVerts)

            # If the vertexId exists in the quad
            if vertIdx in quadVerts:

                # Find those in the quad loop on each side
                quadIdx = quadVerts.index(vertIdx)
                connectedVertIndices.append(quadVerts[(quadIdx-1) % polySize])
                connectedVertIndices.append(quadVerts[(quadIdx+1) % polySize])

        # Return only unique results (we don't care about order)
        return list(set(connectedVertIndices))

    # Subdivide the current mesh by one level
    def subdivide(self):

        # A list of the new quads we will be creating. We will replace the old quads
        # with these when we're done
        newQuads = []

        # These data-structures will hold the intermediary vertices for edge midpoints
        # and face centers. We will need ready access to these after we generate them
        edgeMids = {}
        quadCtrList = []

        oldVertexCount = len(self._vertices)

        # STEP ONE: Generate face points
        # -----------------------------------------------------------
        for quadVerts in self._quads:
            polyCount = len(quadVerts)
            # create the center point
            ctr = vec3(0, 0, 0)
            for idx in quadVerts:
                ctr = ctr.add(self._vertices[idx])
            ctr = ctr.div_f(polyCount)

            centerIdx = self.addVertex(ctr)

            quadCtrList.append(centerIdx)

        # STEP TWO: Generate edge points
        # -----------------------------------------------------------
        for curQuad, quadVerts in enumerate(self._quads, 0):
            polyCount = len(quadVerts)

            # create center points for every edge
            for quadIdx in range(polyCount):

                idx = quadVerts[quadIdx]
                idx2 = quadVerts[(quadIdx+1) % polyCount]

                # For sanity/indexing sake, we always want idx < idx2
                if idx > idx2:
                    tmp = idx
                    idx = idx2
                    idx2 = tmp

                # if we don't have an entry, add one
                if not idx in edgeMids.keys():
                    edgeMids[idx] = {}

                # if we haven't already created this edge midpoint while working
                # on another quad, then build it
                if not idx2 in edgeMids[idx]:

                    # The new edge midpoints will be an average of the terminal vertices as well
                    # as the new face points in the quads this edge straddles

                    # First, find those quads
                    connectedQuads = self.quadsContain(idx, idx2)
                    assert len(connectedQuads) == 2

                    avg = self.midpoint(idx, idx2, quadCtrList[connectedQuads[0]], quadCtrList[connectedQuads[1]])

                    edgeMids[idx][idx2] = self.addVertex(avg)

        # STEP THREE: Modify the existing vertices
        # -----------------------------------------------------------
        for idx in range(oldVertexCount):

                # Modify original edge point according to complex system. Mark it as done
                connectedQuads = self.quadsContain(idx)
                n = float(len(connectedQuads))

                # M1: Generate old coord weight
                m1 = self._vertices[idx]

                # M2: Generate average face points weight
                m2 = self.midpoint(*[quadCtrList[quadIdx] for quadIdx in connectedQuads])

                # M3: Generate average edge points weight
                connectedVertIndices = self.connectedVerts(idx)
                connectedEdgeMids = []

                # Given all vertices that have edges connecting to this current vertex,
                # find and average all of the midpoints
                for connectedVertIdx in connectedVertIndices:

                    # Again, index using the smaller vert index value first
                    if idx < connectedVertIdx:
                        cIdx1 = idx
                        cIdx2 = connectedVertIdx
                    else:
                        cIdx1 = connectedVertIdx
                        cIdx2 = idx

                    connectedEdgeMids.append(edgeMids[cIdx1][cIdx2])

                m3 = self.midpoint(*connectedEdgeMids)

                # Weights (for easy modification)
                # There are many methods of weighing the various elements

                # Technique 1
                #w1 = (n - 3.0) / n
                #w2 = 1.0 / n
                #w3 = 2.0 / n

                # Technique 2
                w1 = (n - 2.5) / n
                w2 = 1.0 / n
                w3 = 1.5 / n

                # Technique 3
                #w1 = ((4.0 * n) - 7.0) / (4.0 * n)
                #w2 = 1.0 / (4.0 * (n * n))
                #w3 = 1.0 / (2.0 * (n * n))

                m1 = m1.mul_f(w1)
                m2 = m2.mul_f(w2)
                m3 = m3.mul_f(w3)

                self._vertices[idx] = m1.add(m2).add(m3)

        # STEP FOUR: Create new quads
        # -----------------------------------------------------------
        for curQuad, quadVerts in enumerate(self._quads, 0):
            polyCount = len(quadVerts)

            # create four new quads in the new quad data-structure
            for quadIdx in range(len(quadVerts)):
                idx0 = quadVerts[(quadIdx-1) % polyCount]
                idx1 = quadVerts[quadIdx]
                idx2 = quadVerts[(quadIdx+1) % polyCount]

                if idx0 < idx1:
                    mpoint1 = edgeMids[idx0][idx1]
                else:
                    mpoint1 = edgeMids[idx1][idx0]

                if idx1 < idx2:
                    mpoint2 = edgeMids[idx1][idx2]
                else:
                    mpoint2 = edgeMids[idx2][idx1]

                centerIdx = quadCtrList[curQuad]

                newQuads.append([centerIdx, mpoint1, idx1, mpoint2])

        # STEP FIVE: Rebuild quads
        # -----------------------------------------------------------
        self._quads = []

        for quad in newQuads:
            self.addQuad(*quad)

    # Snap all vertices to a sphere with the specified radius
    def spherize(self, radius=1.0):
        print "running"
        for i in range(len(self._vertices)):
            vec = self._vertices[i].normalize()
            self._vertices[i] = vec.mul_f(radius)
