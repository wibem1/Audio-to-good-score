# Web-Beta-Prüfung 29.10.2026

## Automatisiert bestanden

- 45 Python-Fälle: 38 Kernverträge/Export/Unabhängiger XML-Prüfer, 7 Browseradapterfälle mit echten mido/music21-Exporten. Keine Export-Mocks. Browseradapter prüft kompakte Pläne, Freikomposition ohne Analysebindung, fehlerhafte Rhythmik, unsichere Voranalyse, Quellenidentität, SHA-256-Fallback und verweigert Codeausführung.
- 50 Node-Fälle: 39 bestehende Kerntests plus 11 Provider-/Umfangsfälle. Fester Anbieterhost, API-Schlüssel im Header, Ausgabelimit, keine automatische Wiederholung, abgeschnittene Antworten abweisen, fehlende Zugangsdaten ohne Netzaufruf, gültige Modellkennung, Modelllisten-Paginierung, JSON statt Python, Nachbarpassagen-/Tempo-/verschachtelter Performance-Schutz.
- 12 frühere Zeit-/Tempo-/MusicXML-Einheitenfälle erneut bestanden.

Originalprotokolle: `python-tests.txt`, `node-tests.txt`, `unit-0.2.txt`.

## Im Cloud-Chromium beobachtet

Mit Sites-Vorschau und tatsächlichen Musikbibliotheken, keine selbst gebaute Browsersteuerung:

- Pyodide lädt music21 9.9.1 und exportiert den synthetischen Plan mit 14 Noten. Beide Ausgabeformate werden im Kern gegen den Plan geprüft.
- Zweiter gültiger Plan per Dateiauswahl importiert; Titelwechsel sichtbar. Rückgängig stellt ursprünglichen Titel wieder her, Wiederherstellen den neuen. Partitur wird bei Fassungswechsel geleert, damit keine alte Fassung angezeigt wird.
- Verovio 5.7.0 rendert echte MusicXML in ein zweisystemiges SVG mit sichtbarem Tempo. Keine fingierte Notenvorschau.
- Automatische Wiederherstellung über Seitenneuladen erfolgreich; Fassungen werden erneut durch den Exporter geprüft.
- Synthetische MIDI per Dateiauswahl importiert; lokale Voranalyse enthält 14 ausdrücklich unsichere Anschläge. Quellenhash wird geprüft. Im HTTP-Preview war WebCrypto nicht verfügbar; geprüfter SHA-256-Fallback im Python-Worker ergänzt.
- Synthetische WAV per Dateiauswahl dekodiert; Audio/MIDI gemeinsam sichtbar. Audio startet mit laufender Positionsanzeige. Wechsel auf MIDI, Stopp und erneuter Start geprüft. Kein menschlicher Hörnachweis behauptet.
- Nutzerhinweis auf veränderte Schlussfigur gespeichert; sichtbar im Gespräch, als unbestätigter Nutzerbefund in neuer Analyserevision. Keine automatische Musikänderung.
- Gemini-Konfiguration mit offensichtlich ungültigem Testplatzhalter nur lokal eingegeben. Kompositionsauftrag öffnet vorher Einzelzustimmung mit Anbieter, Modell, Tokenlimit und Kostenhinweis. **Abbrechen** gewählt; kein Generierungsauftrag freigegeben und kein kostenpflichtiger Aufruf durchgeführt.

## Prüfgrenzen und offene Abnahmen

- Downloadschaltflächen erzeugen korrekte Blob-Links. Die Cloud-Browser-Downloadüberwachung lieferte in der HTTP-Vorschau weder für programmatischen noch direkten Link-Klick eine Datei. Download-UI-Ende-zu-Ende **nicht bestanden/nicht nachgewiesen**, nicht als erfolgreicher Dateidownload zählen. Erzeugte Dateiinhalte sind unabhängig im Kern getestet. Reale Downloads unter HTTPS nach privater Anmeldung offen.
- Produktionsadresse ist erreichbar und zeigt den privaten ChatGPT-Zugang. Cloud-Browser besitzt keine angemeldete Sitzung; Produktionsabläufe hinter dem Zugang daher nicht geprüft. Zugriff wurde nicht auf öffentlich umgestellt.
- Audio-only-Basic-Pitch-Inferenz in dieser neuen Oberfläche nicht erneut vollständig unter HTTPS geprüft; frühere Modellnachweise gehören zum Vorgänger. Voranalyse erfordert sichere Modell-Prüfsummenfunktion. Nicht als neue bestandene Audio-only-Abnahme ausgeben.
- Keine Live-Gemini-Anfrage, keine gemessene Vorlagennähe und keine musikalische Gesamtfreigabe. Keine Abnahme in Dorico/MuseScore des neuen Exporters, keine Safari-/Firefox-/Tablet-Abnahme.
- Technische Tests verhindern definierte Rhythmusfehler; sie beweisen nicht, dass jede KI-Fassung musikalisch dem Original entspricht.

**Ergebnis:** geprüfter technischer Beta-Stand mit ausdrücklich offenen Ende-zu-Ende-/Musikabnahmen. Kein Anspruch, die gesamte musikalische Produktvision sei fertig abgenommen.
