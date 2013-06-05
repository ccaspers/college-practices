# Python OBJ-Viewer

Einfacher Viewer, entstanden als Aufgabe im Sommersemester 2013 der
Hochschule RheinMain. Implementierung von Christian Caspers.

Features:

 * Einlesen von Wavefront-OBJ-Dateien
 * Rotieren, Zoomen, Verschieben 
 * Wechsel zwischen Parallel- und Zentralperspektive
 * Verändern der Darstellungsfarben

Ausführen mittels:
```
python main.py <obj-file>
```
---
###Steuerung

 * Darstellung verändern
   - `F1` - Hintergrundfarbe wechseln
   - `F2` - Wireframefarbe wechseln
   - `F3` - Projektion wechseln

 * Rotation  
   Großbuchstaben: positive Rotation, Kleinbuchstaben negative Rotation
   - `X` - Rotation um X-Achse
   - `Y` - Rotation um Y-Achse
   - `Z` - Rotation um Z-Achse
   - `Linke Maustaste` gedrückt halten und ziehen

 * Zoom
   - `Mittlere Maustate` gedrückt halten und ziehen

 * Verschieben
   - `Rechte Maustate` gedrückt halten und ziehen

---
### Vorraussetzungen

 * NumPy
 * PyOpengl
 * Python 2.7+