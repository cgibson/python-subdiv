# Based on an example found at https://github.com/dasricht/glfwexample
#
# Requires:
#   - glfw lib installed. The glfw module will check in all of the appropriate
#     locations, including GLFW_LIBRARY if such an environment variable exists
#     https://github.com/dasricht/glfwexample
#
#   - python-glm installed. This is only a python implementation of the glm
#     library. https://bitbucket.org/duangle/python-glm
#
# I take no credit for glfw or shaderutil modules, which were kindly offered
# into the public domain by Richard Petri. I am simply utilizing his code
# to display the subd mesh code in the subd module
##############################################################################

import os
import sys
import shaderutil
import time

from glfw import *
from OpenGL.arrays.vbo import VBO
import glm
from mesh import SubdMesh

# Build a cube mesh and subdivide it several times
cubeMesh = SubdMesh.buildCube()
cubeMesh.subdivide()
cubeMesh.subdivide()
cubeMesh.subdivide()
#cubeMesh.spherize()

# Create a flat array of the subdivided mesh data
cubedata = cubeMesh.toFloatArray()

# Window width/height
width = 800
height = 600

# Camera information
up = glm.vec3(0, 1, 0)
eye = glm.vec3(1.0, 1.0, 1.0)
lookAt = glm.vec3(0, 0, 0)

# Global matrices
modelView = glm.mat4.look_at(eye, lookAt, up)
modelViewProjection = None

# Program state
running = True

# Resize window callback
def resizeWindow(w, h):
    global modelViewProjection, modelView, width, height

    # Update width and height
    width = w
    height = h
    glViewport(0, 0, width, height)

    # Update matrices
    perspective = glm.mat4.perspective(70, float(width) / height, 0.1, 10.0)
    modelViewProjection = perspective.mul_mat4(modelView)

# Keypress callback.
def keypress(key, action):
    if key == GLFW_KEY_ESC:
        global running
        running = False
    
if __name__ == "__main__":
    # Something in glfwInit changes the cwd.
    cwd = os.getcwd()
    # Initialize
    if not glfwInit():
        print >> sys.stderr, "Unable to initialize GLFW."
        sys.exit(-1)
    # Restore the old cwd.
    os.chdir(cwd)

    if not glfwOpenWindow(width, height, 0, 0, 0, 0, 32, 0, GLFW_WINDOW):
        print >> sys.stderr, "Unable to open Window."
        glfwTerminate()
        sys.exit(-1)
    glfwSetWindowSizeCallback(resizeWindow)
    glfwSetKeyCallback(keypress)
    glfwSetWindowTitle("OpenGL Subdivision Surface Test")
    glfwEnable(GLFW_AUTO_POLL_EVENTS) # Enables the polling for key/mouse events in the swap buffer function!

    # Print some OpenGL information.
    print "OpenGL Information:"
    for prop in ["GL_VENDOR", "GL_RENDERER", "GL_VERSION", "GL_SHADING_LANGUAGE_VERSION"]:
        print "\t%s = %s" % (prop, glGetString(locals()[prop]))

    # Set up OpenGL Stuff.
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glClearColor(1, 1, 1, 0)
    glPointSize(3)
    # Set up the shader.
    prog = shaderutil.createProgram("./shader.vs", "./shader.fs")
    mvploc = glGetUniformLocation(prog, "mvp")
    colloc = glGetUniformLocation(prog, "color")
    positionloc = glGetAttribLocation(prog, "vs_position")
    
    # Setup VAO
    vertobj = glGenVertexArrays(1)
    glBindVertexArray(vertobj)

    # Setup the VBO
    vertbuf = VBO(cubedata, GL_STATIC_DRAW)
    vertbuf.bind()
    glEnableVertexAttribArray(positionloc)
    glVertexAttribPointer(positionloc, 4, GL_FLOAT, GL_TRUE, 4 * 4, vertbuf+0)
    vertbuf.unbind() # We can unbind the VBO, since it's linked to the VAO

    running = True
    t = time.time()
    rotation = 0.0
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(prog)

        # Generate a temporary matrix with a rotation added to the mix
        # I'm not sure why I have to transpose. If I do not, bad things
        # happen.
        tmp_mat = modelViewProjection.rotate(rotation, glm.vec3(0, 1, 0)).transpose()
        glUniformMatrix4fv(mvploc, 1, GL_TRUE, tmp_mat.to_tuple())

        # RENDER the red fill for the model
        # -----------------------------------------------------------
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

        # Set red fill for mesh
        glUniform4f(colloc, 1, 0, 0, 1)

        # Offset to allow for proper wireframe display
        glEnable( GL_POLYGON_OFFSET_FILL );
        glPolygonOffset( 1, 1 )

        # Draw the cube
        glDrawArrays(GL_QUADS, 0, len(cubeMesh._quads)*4)

        # RENDER the black wireframe for the model
        # -----------------------------------------------------------
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        # Disable offset fill
        glDisable( GL_POLYGON_OFFSET_FILL );

        # Set black color for wireframe
        glUniform4f(colloc, 0, 0, 0, 1)

        # Draw the cube
        glDrawArrays(GL_QUADS, 0, len(cubeMesh._quads)*4)

        # UPDATE the rotation based on render time
        # -----------------------------------------------------------
        rotation += (time.time() - t) / 15 * (2 * 3.1416)
        t = time.time()

        # Stop running if window gets closed.
        running = running and glfwGetWindowParam(GLFW_OPENED)

        glfwSwapBuffers()
        
    glfwTerminate()