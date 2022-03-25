# Cambotprocessor Wiki

## Workflow

Der Workflow des Cambotprocessor läuft über 2 Schnittstellen. Zuerst werden vom Cambotmanager Bilddaten geholt und diese in eine gewählte Outputdirectory gespeichert. Danach lässt der Cambotprocessor die Bilddaten durch Meshroom laufen und speichert das schlussendliche 3D Model ab unter dem Cambotprocessor outputdirectory.

## Schnittstellen
Die Applikation beinhaltet 2 Schnittstellen. Eine Schnittstelle ist zwischen dem Cambotprocessor und dem Cambotmanager welche über eine API überbrückt wird. Die andere Schnittstelle ist zwischen dem Cambotprocessor und Meshroom.
Die API-Brücke beinhaltet einen Call, der Call wird durchgeführt durch eine andere Commandline innerhalb des cambotprocessors. Durch “python APICommunication.py –URL [URL der API] –id [custom ID] –outputdirectory [Directory mit URL output]” kann der Cambotmanager aufgerufen werden und die einzelnen Bilderdaten können werden.


Die Schnittstelle zwischen dem Cambotprocessor und Meshroom wird überbrückt via Commandlines. Meshroom beinhaltet einzelne .exe files welche die einzelnen steps beinhaltet mit ihrem jeweiligen input und output. Somit können wir per Python die exes ausführen und den Standardqueue durchführen.