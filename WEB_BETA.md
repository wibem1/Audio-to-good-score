# MusicCraft App 0.1.0 Beta 2

Zwei eigenständig nutzbare Module: Analyse und Komposition. Die Beta verbindet den geprüften Verarbeitungskern 0.3 mit einer statischen Browseroberfläche. Arbeitsmodus: **Musikalisch ausgewogen**. Sie ist eine technische Erprobung, keine allgemeine musikalische Qualitätsfreigabe.

## Analyseüberarbeitung in Beta 2

Die KI schreibt Rohbefunde nicht erneut aus. Sie ergänzt zwölf musikalische Kriterien sowie gezielte unsichere Stellen; der lokale Kern erstellt daraus die vollständige kompatible Übergabe. Voranalyse, musikalische Interpretation und fehlgeschlagener Versuch sind klar gekennzeichnet. „KI-Aufträge und Verbrauch“ zeigt Eingabe-, Antwort- und Denktokens, soweit gemeldet. „Diagnose speichern“ ist auch ohne Komposition verfügbar. Der manuelle Analyseauftrag ermöglicht denselben Austausch mit einer anderen KI. Keine automatische kostenpflichtige Fortsetzung, Wiederholung oder Limiterhöhung. Details: [Analyseaustausch 1](protocol/ANALYSIS_EXCHANGE_1.md).

## Benutzung

1. Die private Web-App öffnen und mit dem zugehörigen ChatGPT-Konto anmelden. Keine lokale Installation nötig.
2. Für Analyse Audio, MIDI oder beides öffnen, den kurzen Abschnitt anhören und auswählen. **Lokale Voranalyse** liefert bewusst unsichere Notenkandidaten. **Musikalisch mit KI analysieren** benötigt ein eigenes Gemini-Modell und einen API-Schlüssel. Erst den Bericht und die offenen Fragen prüfen; die vollständigen Befunde lassen sich aufklappen und exportieren.
3. **Für Komposition verwenden** übernimmt den Analysestand als Grundlage. Den musikalischen Auftrag formulieren und ausdrücklich beauftragen. Für eine freie Komposition direkt das Kompositionsmodul nutzen, ohne Analysepflicht.
4. Original und Komposition im Player an derselben Zeitposition vergleichen. Partitur anzeigen, MIDI und MusicXML speichern. Änderungen über den aufklappbaren Bereich taktweise beauftragen; geschützte Nachbarpassagen werden maschinell kontrolliert. Fassungen lassen sich rückgängig machen und wiederherstellen.
5. Ein Gespräch verändert keine Musik. **Als Hinweis festhalten** speichert den Wunsch; die Analyse kennzeichnet ihn als Nutzerhinweis. Eine musikalische Änderung braucht einen eigenen Auftrag.
6. **Projekt sichern** speichert Quellen, Befunde und Fassungen zusammen, ohne API-Schlüssel. Zusätzlich wird auf demselben Gerät automatisch gespeichert. Browserdaten sind kein Ersatz für eine eigene Projektdatei.

**Ohne API-Schlüssel:** Lokale Voranalyse, Analyseimport, Übergabeauftrag für eine andere KI, Import eines schema-konformen Composition Plan, lokale Exporte und Partituransicht funktionieren ohne generativen KI-Aufruf. Ein Python-Skript aus einer KI-Antwort wird nicht ausgeführt. Das technische Beispiel ist ausdrücklich synthetisch.

## Kosten und Daten

Jeder generative Auftrag zeigt Anbieter, Modell, übertragenen Kontext, gegebenenfalls die Audiopassage und die maximale Ausgabelänge. Erst das Bestätigen dieses einzelnen Auftrags sendet die Anfrage. Kein automatischer kostenpflichtiger Wiederholungsversuch. Ein Abbruch kann entstandene Kosten nicht zurücknehmen. Die Tokenbegrenzung ist keine garantierte Geldobergrenze; optionale selbst eingetragene Preise und Anbieter-Verbrauchsdaten stehen in der Diagnose.

Originalmusik bleibt im Browser und im selbst gespeicherten Projekt. Nur die ausdrücklich bestätigte KI-Anfrage sendet ausgewählte Daten an Google. Komposition erhält die Analyse und den Auftrag, kein Originalaudio. Die Modellliste wird erst per Schaltfläche mit dem eigenen Schlüssel geladen. Schlüssel standardmäßig nur im Arbeitsspeicher; dauerhafte Speicherung ausschließlich mit der ausdrücklich beschrifteten Option. Projektexport enthält ihn nie.

Der Python-Kern läuft lokal in einem Pyodide-Worker. Beim ersten Start werden Pyodide und Musikbibliotheken aus öffentlichen Paketquellen geladen; das kann länger als eine Minute dauern. Notensatz lädt Verovio vom CDN. Deshalb ist die Beta keine vollständige Offline-App. Originale werden nicht überschrieben. Die private Veröffentlichung enthält weder Nutzer-Musikdateien noch Schlüssel.

## Technisches Profil und Grenzen

- Browser: Chromium geprüft; Safari, Firefox und native Tablets noch nicht abgenommen.
- Kern: Analyse/Composition Plan 0.3, exakte gekürzte Brüche, Zeit- und Quellenbindung, Inhalt/Gestaltung getrennt. Kompakte Tabellen sind verlustfrei, Lücken keine Pausen.
- Klavierprofil, höchstens 2000 Viertelnoten-Einheiten und 20 Fassungen pro Projekt. Stimmen monophon oder gleich lange Akkorde; unabhängige Dauern verlangen eigene Stimmen. KI-Ausgaben außerhalb dieses Profils werden abgewiesen.
- Audio höchstens 50 MiB; MIDI/Plan 10 MiB; Analyse 5 MiB; Projekt 100 MiB. Ausgewählte Audioanalyse höchstens 60 Sekunden. Für erste musikalische Versuche kurze Phrasen verwenden.
- Lokale MIDI-/Basic-Pitch-Auswertung ist **keine** vollständige musikalische Analyse. Tonart, Metrum, Form, Stil, Melodieführung und Begleitung werden dadurch nicht als sicher erkannt ausgegeben.
- MIDI und MusicXML entstehen aus demselben validierten Plan. Unabhängige Prüfungen kontrollieren Zeiten, Taktfüllung, Tempo und Tonmaterial. Dies beweist weder Vorlagennähe noch musikalische Qualität.
- Player nutzt einen einfachen identischen Vergleichsklang für beide MIDI-Fassungen. A/B ist zeitbezogen; bei abweichender Form oder Tempogestaltung besteht keine automatisch geschätzte Taktzuordnung zur Aufnahme.
- Partitur ist seitenweise sichtbar; **Diese Seite drucken / PDF** druckt die aktuelle Seite. Vollständige Partitur über MusicXML im Notationsprogramm öffnen.
- Live-Gemini-Anfragen, modellabhängige Audioerkennung und musikalische Nachkompositionsqualität sind ohne freigegebenen Schlüssel/Kostenauftrag **nicht abgenommen**. Weitere Anbieter können über den Dateiaustausch teilnehmen; keine native Gemini/Claude/OpenAI-Vollabdeckung behaupten.
- Reale Dorico-/MuseScore-Abnahme des neuen Kernexporters sowie menschlicher Hörvergleich bleiben offen.

## Reproduktion für Entwickler

```sh
python3 -m pip install -r requirements-composition.txt
python3 -m unittest discover -s tests -p 'test_*.py' -v
npm test
python3 web/build.py
```

`web/build.py` erzeugt `dist/`; ein anderes Ziel ist mit `--output /absoluter/pfad` möglich. Statisch unter HTTPS bereitstellen. Projektkennung steht in `.openai/hosting.json`, niemals eine zweite Site für Updates anlegen. Pyodide 0.29.1 lädt music21 9.9.1, mido 1.3.3 und jsonschema 4.26.0; Verovio 5.7.0 rendert die erzeugte MusicXML. `web/core-worker.js` verarbeitet ausschließlich feste JSON-Aktionen, keinen Modellcode.

Aktuelle Nachweise und Abnahmegrenzen: `test-results/analysis-redesign/`; frühere Beta-1-Prüfungen in `test-results/web-beta/`. Der ältere Einzelnoten-/Reparaturprototyp im Repository bleibt historisch erhalten; die neue Web-App wird aus `web/` gebaut.
