# MusicCraft core 0.3 – implementierter Umfang

29.10.2026. Eigenständig geprüfter Verarbeitungskern, keine neue freigegebene Web-App-Version. Ablösung der bloßen 0.2-Protokollbeschreibung durch maschinenprüfbare Verträge.

## Übernommene Ideen und Bausteine

- Inhalt und Gestaltung getrennt, angeregt durch Audio-to-symbolic Arrangement/BOSSA: `content` umfasst Struktur, Harmonie, Tonkandidaten und Rhythmik, `style` Ausdruck/Charakter. Keine spielbare Analyse vorausgesetzt.
- Kompakte Spaltentabellen als verlustfreie Transportdarstellung für Beobachtungen und komponierte Ereignisse. Konzeptionell an symbolischen Eventdarstellungen wie REMI/MidiTok orientiert, kein Code daraus kopiert und keine Modell-Tokenkompatibilität behauptet. Presence-Maske unterscheidet fehlende Felder von null. Beispiel: 1533 statt 2155 Bytes bei identischer kompakter JSON-Serialisierung (~29%). Keine pauschale Tokenkosten-Garantie.
- Bis zu drei lokale Tonalternativen einer unsicheren Stelle zur musikalischen Beurteilung. Keine automatische Korrektur, kein implementiertes musikalisches Ranking oder vollständiges Inpainting. Sichere Befunde werden nicht überschrieben.
- `music21` 9.9.1 für Notation/MusicXML, `mido` 1.3.3 für SMF, `jsonschema` 4.26.0 für JSON-Schema. Kein vom Modell frei erzeugter XML-/MIDI-Bytecode nötig. Versionen in `requirements-composition.txt`. Optionaler lokaler Python-Prozess, noch keine Browser-/Server-Anbindung.

## Verträge

`analysis.schema.json` und `composition.schema.json`, JSON Schema Draft 2020-12, jeweils Version 0.3. Syntaxprüfung plus semantische Prüfungen in `musiccraft/contracts.py`. Kein Fernabruf von Schemas. Keine Netzwerk-/KI-Aufrufe im Kern.

Analyse: mehrere Quellen mit eigener Sekundenachse/Prüfsumme, eigener Abschnittszuordnung; unbekannte Tonhöhe oder leere Kandidatenliste erlaubt. Kandidatenbeziehung ausdrücklich `alternatives`, `simultaneous` oder `unresolved`. Abschnittsentwicklung in Worten, globale/gestalterische Befunde mit Begründung, Herkunft und Abhängigkeiten. Abhängige Befunde dürfen nicht sicherer als ihre Voraussetzungen sein. Metrische Hypothesen mit exakten Brüchen und überprüfter Puls-/Tempo-Gleichung.

Komposition: freie neue Komposition ohne Analyse möglich; Imitation/Revision erfordern die genaue validierte Analyserevision und kanonischen JSON-SHA256 (UTF-8, sortierte Schlüssel, keine Leerzeichen). Stimmen, Takte, Tempoereignisse, Noten, explizite Pausen und Entscheidungen sind eindeutig. `_q` immer Viertelnoten-Einheiten, Brüche vollständig gekürzt. Alle hinzugefügten Töne haben einen Entscheidungsverweis; musikalische Begründung bleibt Aufgabe des Komponisten.

Eine Stimme ist monophon oder eine Folge gleich langer Akkorde. Unabhängig überlappende Dauern erfordern eigene Stimmen. Tonbereich des aktuellen Klavier-Exportprofils A0–C8, zwei Systeme; MIDI-Kanal 10 ausgeschlossen. Bis 10000 Noten und 2000 Viertelnoten. Teil-/Auftakte ausdrücklich begründen, Tempowechsel als geordnete Map. MIDI-Auflösung wird aus allen rationalen Zeiten exakt bestimmt; übermäßige Auflösung wird abgelehnt. Optionale Performance-Zeiten in Sekunden sind getrennt vom Score. Gleiche Tonhöhe im selben Kanal darf nicht überlappen. Kein stilles Quantisieren.

`compact.pack/unpack` ist ein verlustfreier Codec, kein Validator: nach Auspacken das passende Vertragsprüfverfahren verwenden. Erweiterte künftige Gestaltung (Pedal, Artikulationen, Ornamente, Instrumentwechsel) ist noch nicht im implementierten Profil; unbekannte Felder werden abgelehnt statt ignoriert. Vorlagen mit diesen Merkmalen nicht als vollständig erhalten ausgeben.

0.2-Migration ist ausdrücklich aufzurufen. Die zwei privaten Testübergaben wurden migriert: je 48 Beobachtungen erhalten; Originalquellen dabei nicht geöffnet. Alte Formatfassung bleibt vorhanden. Fehlt eine Begründung im alten Datensatz, wird Sicherheit auf undetermined gesetzt, statt einen Beleg zu erfinden. Nicht alle Metadaten der alten Versuchshülle werden übernommen; die neue Provenienz benennt Migration und Grenzen.

## Export und Kontrolle

Gemeinsamer Plan → mido-SMF und music21-MusicXML. Notation darf gebundene Noten an Taktgrenzen teilen; Vergleich führt Bindungen wieder zusammen. Zweites XML-Prüfverfahren mit ElementTree rekonstruiert Zeitachsen unabhängig von music21, inklusive backup/chord, Stimmenfüllung, Notentyp, Punktierungen, Tuplets, Tempo und Systemen. MIDI wieder mit mido einlesen und gegen Plan/Performance-Zuordnung prüfen. Dokumentierte Toleranzen: MIDI-Tempo-Rundung maximal 0,5 Mikrosekunden pro Viertel, Performance-Rundung maximal 0,5 Tick. Notierte Zeiten werden nicht gerundet.

Tempoanzeige als expliziter Text „Viertel = …“ (2 Dezimalstellen); MusicXML sound tempo behält volle Berechnungspräzision. Das vermeidet nicht verfügbare Tempo-Sonderglyphen in SVG/PDF-Renderern. Bibliotheksgenerierte technische XML-IDs/Datumsfelder sind nicht byteidentisch reproduzierbar, musikalische Ereignisse hingegen prüfbar.

Erst nach bestandenen Prüfungen werden Ausgabedateien übernommen. Vertrags-/Exportvalidierungsfehler verändern vorhandene Ausgaben nicht. Das ist keine über mehrere Dateien transaktionssichere Speicherung gegen Betriebssystem-/Stromausfälle. Originalquellen bleiben unangetastet. Prüfbericht enthält tatsächlich ausgeführte Tests; menschliches Hören bleibt not_run.

## Reproduktion (Entwicklerwerkzeuge)

```sh
python3 -m pip install -r requirements-composition.txt
python3 -m unittest discover -s tests -p test_composition_core.py -v
python3 tests/test_handoff_units.py
npm test
python3 -m musiccraft validate-plan tests/fixtures/composition-plan.json
python3 -m musiccraft export tests/fixtures/composition-plan.json /tmp/musiccraft-export
python3 -m musiccraft migrate-02 /path/audio-handoff-v0.2.json /path/audio-handoff-v0.3.json
python3 -m musiccraft validate-analysis /path/audio-handoff-v0.3.json
python3 -m musiccraft alternatives /path/audio-handoff-v0.3.json
python3 -m musiccraft pack /path/audio-handoff-v0.3.json /path/audio-compact.json
```

Für vorlagenbezogenen Export `--analysis /path/analysis.json` ergänzen. Migration/Pack schreiben ausschließlich neue Dateien (kein Überschreiben). Ein Export braucht bereits einen komponierten Plan; dieser Kern komponiert nicht automatisch. Die CLI ist keine neue Endanwender-Bedienung und ersetzt nicht die geplante Weboberfläche.

## Teststand und nächste Schritte

38 neue Tests, 12 frühere Einheitenfälle, 39 bestehende JS-Kerntests bestanden. Abgedeckt: stale Analyse, fehlende Quellenbindung, Unsicherheitsabhängigkeiten, unzulässige Zeitwerte, Triolen, punktierte Dauern, Taktwechsel, Auftakt, Bindungen, Pausen, einhändige Fassung, Performance-Gates/Überlagerungen, Erhalt alter Ausgaben bei Ablehnung und schädlich veränderte XML-Tempo-/Dauerwerte. Drei synthetische Fälle in Verovio 5.7.0 gerendert, finale Ansicht mit bereinigter Tempoanzeige geprüft; keine Dorico-/MuseScore-Abnahme des neuen Exporters, keine menschliche Hörprüfung.

Offen: Web-Anbindung mit Player/Chat, tatsächliche KI-Analyse und KI-Komposition/Ranking, weitere Ausdrucksparameter, unabhängiger externer 0.3-Modelltest. SheetSage/BOSSA/Audio2MIDI nicht installiert oder als geeignet behauptet. Größere Modellintegration bleibt Vergleichsaufgabe mit separater Lizenz-/Hardwareprüfung. Keine kostenpflichtigen Aufrufe erfolgt.

## Quellen und Lizenzgrenzen

- https://arxiv.org/abs/2112.15110 – Audio-to-symbolic Arrangement.
- https://zhaojw1998.github.io/bossa/ – Inhalt/Stil, Modell-/Demo-Kontext.
- https://miditok.readthedocs.io/en/latest/tokenizations.html – REMI und verwandte Repräsentationen.
- https://eita-nakamura.github.io/articles/Hiramatsu_etal_TranscriptionCorrection_ICASSP2021.pdf – alternative Korrekturkandidaten, begrenzter Gesangskontext.
- https://music21.org/music21docs/ – music21, BSD-Lizenz laut installierten Paketmetadaten; Corpus-Dateien haben ggf. separate Bedingungen und werden nicht verwendet/mitgeliefert.
- https://github.com/mido/mido – mido, MIT; Paketlizenz im installierten Wheel.
- https://github.com/python-jsonschema/jsonschema/blob/main/COPYING – jsonschema, MIT.

Es wurde kein Code/Gewicht aus den Forschungsprojekten kopiert. Abhängigkeiten werden installiert, nicht in diesem Repository vendort. Diese Entscheidung ersetzt keine Lizenzprüfung etwaiger späterer Modelle oder Trainingsdaten.
