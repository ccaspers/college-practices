uniform vec4 ambientColor;
uniform vec4 diffuseColor;
uniform vec4 specularColor;
uniform vec3 lightPosition;
uniform mat4 mvpMatrix;
uniform mat4 mvMatrix;
uniform mat3 normalMatrix;

varying vec4 varyingColor;

void main() {
    vec3 eyeNormal = normalize(normalMatrix * gl_Normal);

    vec4 vPosition4 = mvMatrix * gl_Vertex;
    vec3 vPosition3 = vPosition4.xyz / vPosition4.w;
    vec3 vLightDir = normalize(lightPosition - vPosition3);
    float diff = max(0.0, dot(eyeNormal, vLightDir));
    varyingColor = diff * diffuseColor;
    varyingColor += ambientColor;

    vec3 reflection = normalize(reflect(-vLightDir, eyeNormal));
    float spec = max(0.0, dot(eyeNormal, reflection));
    if(diff != 0.0){
        float fSpec = pow(spec, 128.0);
        varyingColor.rgb += vec3(fSpec, fSpec, fSpec);
    }
    gl_Position = mvpMatrix * gl_Vertex;
}