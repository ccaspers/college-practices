import re

def parse(objFile):
    contents = file(objFile).readlines()
    
    v = parseVertices(contents)
    vt = parseTextureCoordinates(contents)
    vn = parseNormals(contents)
    vp = parseParameterSpaceVertices(contents)
    f = parseFaces(contents)
    
    return {"v" : v,
            "vt": vt,
            "vn": vn,
            "vp": vp,
            "f" : f}
    
def parseVertices(contents):
    return parseCoordinates(contents, "v")

def parseTextureCoordinates(contents):
    return parseCoordinates(contents, "vt")

def parseNormals(contents):
    return parseCoordinates(contents, "vn")

def parseParameterSpaceVertices(contents):
    return parseCoordinates(contents, "vp")

def parseFaces(contents):
    return []

def parseCoordinates(contents, prefix):
    lines =  extractMatch(contents, prefix + " .")
    return [makeCoordinatesFrom(line, prefix) for line in lines]

def extractMatch(list, pattern):
    return [t for t in list if re.match(pattern, t)]

def makeCoordinatesFrom(line, replace):
    return tuple([float(x) for x in line.strip(replace+" ").split()])
