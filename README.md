# Cambotprocessor

## Benutzerdokumentation

### Vorbereitungen für Ausführung

Um Cambotprocessor auszuführen müssen einige Dependencies installiert sein diese beinhalten:
- configparser (V5.0.0<)
- imutils (V0.5.4<)
- opencv-python (V4.5.5.62<)
- requests (V2.27.1<)
- numpy (V1.21.5<)
- meshio (V5.3.4<)

Diese dependencies können in einer Pythonumgebung mit "pip install" installiert werden.

Ebenfalls muss Meshroom installiert werden (Verfügbar unter https://alicevision.org/#meshroom) 

## Schnellstart

Der Cambotprocessor wird via "python cambotprocessor.py" ausgeführt.

Um Cambotprocessor auszuführen müssen einige Parameter mitgegeben werden

- --config: Beinhaltet Eingaben für alle anderen Parameter damit diese gespeichert werden können (optional)
- --blur: Bestimmt Grenze, ab welcher ein Bild aus der Bilddirectory entfernt werden sollte, da ein Bild zu blurry ist und zu unklar, um zu erkennen.
- --outputtype: Bestimmt Fileending in welche das 3d Model gespeichert werden sollte.
- --meshroomqueue: Beinhaltet gesamte Commandlinequery zum Ausführen einer komplett modifizierbaren Meshroom-queue (optional)
- --bounding Erstellt eine Boundingbox welche Abschnitte ausserhalb der definierten Box entfernt mit jeweils 5 Parameter. X: Länge der Box auf der X-Achse, Y: Länge der Box auf der Y-Achse, Z: Länge der Box auf der Z-Achse, Euler: Rotation der Box in Euler, S: Skalierung der Box in XYZ (optional)
- --input: Directory von Bildern welche für Meshroomqueue genutzt werden
- --output: Directory in welchen das Endprodukt gespeichert wird (3d Model + Texturing Datei)
- --binary: Directory der Binary von Meshroom zum Ausführen von Meshroomfunktionen (auffindbar unter der Meshroom-Installation/aliceVision/bin)

Alle nicht optionalen Parameter müssen angegeben werden um den Prozess durchzuführen, je nach der Anzahl Bilder und Bildergrösse kann der Prozess bis zu mehrere Stunden benötigen.

Das schlussendliche Resultat wird unter der --output Directory abgespeichert mit den einzelnen zwischenschritten welche der Cambotprocessor benötigt.

## Interaktion mit Cambotmanager

Um neue Bildersets herunterzuladen kann der Nutzer diese vom Cambotmanager herunterladen. Hier gibt es wieder ein verfügbaren Command nämlich "python APICommunication.py". Dieser benötigt auch einige Parameter:

- --URL: URL der API des cambotmanagers
- --id: UUID eines Inventoryitems, das Inventoryitem unter der genannten Id wird gepullt
- --outputdirectory: Directory wo Bilderdaten gespeichert werden, später als –-input bei dem Cambotprocessor Command nutzen

## Cambot Parameter

Dies hier sind nochmal die Parameter und die einzelnen Syntax und Beispiele

| Name          | InputSyntax   | Beispiel     | Beschreibung  |
| ------------- |---------------|--------------|---------------|
| --config     |string (Filedirectory)  | --config «./cambotprocessor.ini» | Beinhaltet Eingabenfür alle anderen Parameter damit diese gespeichert werden können (optional)
| --blur      | float    | --blur 100 | Bestimmt Grenze, ab welcher ein Bild aus der Bilddirectory entfernt werden sollte, da ein Bild zu blurry ist und zu unklar, um zu erkennen.
| --outputtype     | string (fileending)     | --outputtype «stl» | Bestimmt Fileending in welche das 3d Model gespeichert werden sollte.
| --meshroomqueue | string[] | --meshroomqueue [ “/aliceVision_cameraInit.exe –defaultFieldOfView 45 –verboseLevel info –allowSingleView 1 –imageFolder ./Bilder –output cameraInit.sfm” , “/aliceVision_featureExtraction.exe –describerTypes sift –forceCpuExtraction True –verboseLevel info –rangeStart 0 –rangeSize 100 –input camerainit.sfm –output ./ ] | Beinhaltet gesamte Commandlinequery zum Ausführen einer komplett modifizierbaren Meshroom-queue (optional)
| --bounding | string (X,Y,Z,Euler,Scale) | --bounding 10,10,10,0,0,0,1,1,1 | Erstellt eine Boundingbox welche Abschnitte ausserhalb der definierten Box entfernt mit jeweils 5 Parameter. X: Länge der Box auf der X-Achse, Y: Länge der Box auf der Y-Achse, Z: Länge der Box auf der Z-Achse, Euler: Rotation der Box in Euler, S: Skalierung der Box in XYZ (optional)
| --input | string (Filedirectory) | --output «./bilder» | Directory von Bildern welche für Meshroomqueue genutzt werden
| --output | string (Filedirectory) | --output «./result» | Directory in welchen das Endprodukt gespeichert wird (3d Model + Texturing Datei)
| --binary | string (Filedirectory) | --binary «./aliceVision/bin | Directory der Binary von Meshroom zum Ausführen von Meshroomfunktionen




## Parameter APICommunication

| Name          | InputSyntax   | Beispiel     | Beschreibung  |
| ------------- |---------------|--------------|---------------|
| --URL     | string (URL)     | --URL http://www.cambotmanager.ch/api | URL der API des cambotmanagers
| --id      | string   | --id M1l41K5234! | UUID eines Inventoryitems, das Inventoryitem unter der genannten Id wird gepullt
| --outputdirectory      | string (Filedirectory)    | --outputdirectory ./inventory/ | Directory wo Bilderdaten gespeichert werden, später als –input bei dem Cambotprocessor Command nutzen

