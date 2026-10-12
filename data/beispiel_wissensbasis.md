# Beispiel-Wissensbasis: Fahrzeugdiagnose

## DoIP

Diagnostics over Internet Protocol, kurz DoIP, transportiert Diagnosekommunikation über IP-Netzwerke. In einem Testaufbau können Tester und Steuergerät über Ethernet miteinander kommunizieren.

## UDS

Unified Diagnostic Services, kurz UDS, definiert Diagnosedienste. Beispiele sind der Wechsel einer Diagnosesitzung, Tester Present sowie der Transfer von Datenblöcken.

### Tester Present

Tester Present hält eine aktive Diagnosesitzung aufrecht. Der Dienst wird zyklisch gesendet, wenn eine Sitzung nicht wegen Inaktivität beendet werden soll.

### Dateiübertragung

Bei einer Dateiübertragung wird eine Datei typischerweise in mehrere Blöcke geteilt. Die Empfängerseite setzt diese Blöcke wieder zusammen und kann anschließend die Integrität prüfen.

## RAG-Bezug

In diesem Lernprojekt wird dieses Markdown-Dokument geladen, nach Überschriften strukturiert, in überlappende Chunks geteilt und in einer Vektordatenbank gespeichert. Eine Frage ruft passende Textstellen ab, bevor das lokale Sprachmodell die Antwort formuliert.
