# Projektanweisungen – MusicCraft App

Vor jedem Entwicklungsauftrag zuerst die globalen Regeln [DEVELOPMENT_STANDARDS.md](https://github.com/wibem1/AI-Development-Standards/blob/main/DEVELOPMENT_STANDARDS.md) und [AGENTS.md](https://github.com/wibem1/AI-Development-Standards/blob/main/AGENTS.md) vollständig lesen. Danach dieses Dokument, [PROJECT_STATE.md](PROJECT_STATE.md), [TODO.md](TODO.md) und den für den Auftrag relevanten Code prüfen. GitHub ist die verbindliche Quelle des Projektstands.

## Verbindliche Produktausrichtung (29.10.2026)
- Repository: `wibem1/MusicCraft-App`, ehemals `wibem1/Audio-to-Good-Score`. Produktname: **MusicCraft App**.
- Zwei eigenständig nutzbare Module: **Analyse** und **Komposition**. Audio to Good Score bleibt ein Anwendungsfall. Analyse von Audio, MIDI oder beidem; Komposition umfasst Nachkomposition, gezielte Überarbeitung und neue Werke aus Motiven/Vorgaben.
- Vor jeder vorlagenbezogenen Nachkomposition: Analysebericht mit begründeter Sicherheit je Kriterium und Takt/Zeitabschnitt, Unsicherheiten und erwartbarer Vorlagennähe zeigen. Erst ausdrücklicher Nutzerauftrag löst die Komposition aus. Freie Komposition ohne Vorlage benötigt keine vorgetäuschte Analyse.
- Jede Phrase erneut prüfen: Wiederholung und Veränderung durch die Quelle begründen. Keine automatische Musterfortsetzung; ungewöhnliche MIDI-Ereignisse nicht allein wegen stilistischer Erwartungen als Fehler entfernen.
- Einfache Oberfläche: Kurzurteil und Handlungsoptionen zuerst; Kriterien und Taktmatrix aufklappbar. Keine Pflicht, jeden Takt oder jede Note einzeln abzunehmen.
- Diese Zielarchitektur ist **geplant, nicht implementiert**. Bestehende technische Nachweise sind davon getrennt zu führen. Details und Abnahmefälle: Pflichtenheft Abschnitt 12.

## Fachliche Leitplanken
- Die Anwendung unterstützt drei gleichrangige Eingangswege: Audio allein, Audio+MIDI sowie MIDI allein.
- Arbeitsmodus standardmäßig **Musikalisch ausgewogen**: musikalische Substanz (Melodie, Rhythmus, Harmonik, Charakter) erhalten; begründete moderate Änderungen sind erlaubt. Keine unkontrollierte Neukomposition.
- Originaldateien nie überschreiben. Jede Korrektur muss begründet, sichtbar, vergleichbar und rückgängig sein.
- Expressive Aufführungszeiten und rhythmisch lesbarer Notensatz sind unterschiedliche Darstellungen derselben musikalischen Interpretation.
- Technische Validität ist keine musikalische Freigabe. Erforderlich sind musikalische Prüfung, A/B-Hörvergleich und realer Importtest von MusicXML in Zielprogrammen vor entsprechenden Erfolgsbehauptungen.
- Keine pauschale Quantisierung oder blindes Entfernen der MIDI-Tempokurve. Vor jeder Änderung Diagnose der Ursache.
- Keine behaupteten Hörprüfungen ohne tatsächlich durchgeführten Nachweis.
- Keine kostenpflichtigen KI-Aufrufe ohne ausdrückliche Zustimmung; vor Auftrag Kostenschätzung/Limit anzeigen, tatsächliche Aufrufe und Kosten protokollieren.

Siehe [PFLICHTENHEFT_V0.1.md](PFLICHTENHEFT_V0.1.md) für detaillierte Kriterien, Funktionen und Abnahmetests.


