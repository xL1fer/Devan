#version 330

precision mediump float;

in vec3 vNormal;
in vec3 fragPos;

uniform vec3 cameraPosition;

out vec4 out_color;

uniform struct {
  vec4 ambient;
  vec4 diffuse;
  vec4 emission;
  vec3 specular;
  float shininess;

  // These properties are new in 1.10.
  vec4 baseColor;
  float roughness;
  float metallic;
  float refractiveIndex;
} p3d_Material;

uniform struct {
  vec4 ambient;
} p3d_LightModel;

uniform struct p3d_LightSourceParameters {
  // Primary light color.
  vec4 color;

  // Light color broken up into components, for compatibility with legacy
  // shaders.  These are now deprecated.
  vec4 ambient;
  vec4 diffuse;
  vec4 specular;

  // View-space position.  If w=0, this is a directional light, with the xyz
  // being -direction.
  vec4 position;

  // Spotlight-only settings
  vec3 spotDirection;
  float spotExponent;
  float spotCutoff;
  float spotCosCutoff;

  // Individual attenuation constants
  float constantAttenuation;
  float linearAttenuation;
  float quadraticAttenuation;

  // constant, linear, quadratic attenuation in one vector
  vec3 attenuation;

  // Shadow map for this light source
  sampler2DShadow shadowMap;

  // Transforms view-space coordinates to shadow map coordinates
  mat4 shadowViewMatrix;
} p3d_LightSource[2];

uniform sampler2D p3d_Texture0;

// Input from vertex shader
in vec2 texcoord;

// Output to the screen
out vec4 p3d_Color;

void main() {
  // ambient
  float ambientStrength = 0.3;
  vec4 ambient = ambientStrength * p3d_Material.ambient * p3d_LightSource[0].color;

  // diffuse
  vec3 norm = normalize(vNormal); //interpolated normals might not be normalized

  vec3 lightDir;

  vec4 diffuse;
  diffuse.xyzw = vec4(0.0, 0.0, 0.0, 0.0);

  for (int i = 0; i < 2; i++)
  {
    if (p3d_LightSource[i].position[3] == 0.0)    // directional light
        lightDir = normalize(p3d_LightSource[i].position.xyz);
    else
        lightDir = normalize(p3d_LightSource[i].position.xyz - fragPos);

    float diff = max(dot(norm, lightDir), 0.0);

    diffuse += diff * p3d_Material.diffuse * p3d_LightSource[i].color;
  }

  // specular
  float specularStrength = 0.8;
  vec3 viewDir = normalize(cameraPosition - fragPos);
  vec3 reflectDir = reflect(-lightDir, norm);
  float spec = pow(max(dot(-viewDir, reflectDir), 0.0), p3d_Material.shininess/2);

  vec4 specular;
  specular.xyzw = vec4(0.0, 0.0, 0.0, 0.0);
  for (int i = 0; i < 2; i++)
  {
    specular += specularStrength * spec * vec4(p3d_Material.specular, 1.0) * p3d_LightSource[i].color;
  }
  
  p3d_Color = max(diffuse + specular, ambient);
  //vec4 color = texture(p3d_Texture0, texcoord);
  //p3d_FragColor = color.bgra;
}