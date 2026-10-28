# Projektanweisungen – Audio to Good Score

Vor jedem Entwicklungsauftrag zuerst die globalen Regeln [DEVELOPMENT_STANDARDS.md](https://github.com/wibem1/AI-Development-Standards/blob/main/DEVELOPMENT_STANDARDS.md) und [AGENTS.md](https://github.com/wibem1/AI-Development-Standards/blob/main/AGENTS.md) vollständig lesen. Danach dieses Dokument, [PROJECT_STATE.md](PROJECT_STATE.md), [TODO.md](TODO.md) und den für den Auftrag relevanten Code prüfen. GitHub ist die verbindliche Quelle des Projektstands.

## Fachliche Leitplanken
- Die Anwendung unterstützt drei gleichrangige Eingangswege: Audio allein, Audio+MIDI sowie MIDI allein.
- Arbeitsmodus standardmäßig **Musikalisch ausgewogen**: musikalische Substanz (Melodie, Rhythmus, Harmonik, Charakter) erhalten; begründete moderate Änderungen sind erlaubt. Keine unkontrollierte Neukomposition.
- Originaldateien nie überschreiben. Jede Korrektur muss begründet, sichtbar, vergleichbar und rückgängig sein.
- Expressive Aufführungszeiten und rhythmisch lesbarer Notensatz sind unterschiedliche Darstellungen derselben musikalischen Interpretation.
- Technische Validität ist keine musikalische Freigabe. Erforderlich sind musikalische Prüfung, A/B-Hörvergleich und realer Importtest von MusicXML in Zielprogrammen vor entsprechenden Erfolgsbehauptungen.
- Keine pauschale Quantisierung oder blindes Entfernen der MIDI-Tempokurve. Vor jeder Änderung Diagnose der Ursache.
- Keine behaupteten Hörprüfungen ohne tatsächlich durchgeführten Nachweis.
- Kostenpflichtige KI-Aufrufe nur kontrolliert und protokolliert.

Siehe [PFLICHTENHEFT_V0.1.md](PFLICHTENHEFT_V0.1.md) für detaillierte Kriterien, Funktionen und Abnahmetests.
