#version 150

uniform mat4 mvp;
uniform vec4 color;

in vec4 vs_position;
out vec4 fs_color;

void main() {
  fs_color = color;
  gl_Position = mvp * vs_position;
}