# MusicCraft-Übergabeprotokoll 0.2

Status: experimenteller, normativer Datenvertrag; ersetzt Pilot 0.1 für neue Versuche. Noch keine App-Integration oder allgemeine musikalische Abnahme. Versionsnummer betrifft das Format, nicht eine neue App-Version.

## 1. Zwei getrennte Verträge

**A – Analysis Handoff 0.2:** Was lässt sich erkennen? Kurzanalyse plus kompakte Befundtabellen. Darf lückenhaft und mehrdeutig sein. Enthält weder verbindliche Notendauern noch eine vollständige spielbare Stimmenzuordnung. Die Analyse muss keine Partitur erzeugen.

**B – Composition Plan 0.2:** Welche musikalische Fassung entscheidet der Komponist? Eigenständiger, spielbarer Plan mit eindeutigen Stimmen, Einsätzen, Dauern, Tempo und ergänzten Details. Erst hier werden offene Analysefragen aufgelöst. MIDI und MusicXML sollten durch einen gemeinsamen geprüften Exporter daraus abgeleitet werden. Dieser Exporter ist Zielarchitektur, durch dieses Dokument nicht implementiert.

Reine Analyse bleibt ohne Komposition nutzbar. Freie Komposition benötigt keinen Analyseinput. Vorlagenbezogener Auftrag verweist auf eine konkrete Analyse-ID/Revision/Prüfsumme; eine neue Revision erzeugt keine automatische kostenpflichtige Neugenerierung.

## 2. Gemeinsame Einheiten und Grundregeln

- Zeitangaben der Quelle: `time_s`, Sekunden relativ zur unveränderten Quelldatei. Keine Interpretation als MIDI-Ticks oder Schläge. Bei mehreren Quellen eigene Quellen-IDs und explizite Alignment-Anker; kein stillschweigendes Gleichsetzen ihrer Zeitachsen.
- Musikalische Zeiten: `_q` bedeutet **Viertelnoten-Einheiten**, unabhängig von der Taktart. Ganze=4, Halbe=2, Viertel=1, Achtel=1/2, Sechzehntel=1/4, punktierte Viertel=3/2, Achteltriole=1/3.
- Exakte Brüche als `[Zähler, Nenner]`, ganze Zahlen, Nenner positiv, vollständig gekürzt. Keine Brüche als gerundete Float-Werte. Sekundenmessungen dürfen nichtnegative JSON-Zahlen sein, inklusive ihrer Messunsicherheit; null bedeutet unbekannt, nicht 0 Sekunden.
- Tonhöhe: MIDI 0–127, C4=60. Optionale Schreibweise separat; unbekannte Tonhöhe=null. Lautstärke, Spektralstärke oder Modellaktivierung sind keine Erkennungswahrscheinlichkeiten.
- `unknown` ist keine Pause. `alternatives` sind nicht gleichzeitig gespielte Töne. Nur ausdrücklich gleichzeitige Befunde dürfen als Akkord behandelt werden. Ungeordnete Tongruppe, geordnete Folge und Alternativen unterscheiden.
- Keine automatische Musterfortsetzung. Befunde zur Entwicklung je Phrase beachten; Übereinstimmung wiederholter Figuren muss belegt sein.
- Herkunft `observation`, `interpretation`, `user_hint` getrennt halten. Sicherheit: `high`, `medium`, `low`, `undetermined`, mit Begründung; Abhängigkeiten weiterreichen.

## 3. Vertrag A – Analysis Handoff

Pflichtfelder:

| Feld | Festlegung |
|---|---|
| `format`, `version` | `MusicCraft-Analysis-Handoff`, `0.2` |
| `analysis_id`, `revision` | stabile Zeichenkette, positive Ganzzahl |
| `source` | Art audio/midi, Name, SHA256, untersuchter Sekundenbereich |
| `access_policy` | Quellenzugriff erlaubt oder nicht; Quellenidentität ist keine Zugriffserlaubnis |
| `summary` | knappe musikalische Analyse |
| `units` | Zeiteinheit, Tonhöhenkonvention, Definition von `_q` |
| `timing` | beobachtete Pulsspanne/Intervall; ausdrücklich optionale metrische Deutungen |
| `global_findings` | Tonalität, Besetzung/Stil und weitere Befunde mit Sicherheit/Begründung |
| `groups` | Phrasen-/Zeitgruppen, ggf. vorläufige Takte, Harmonie/Bass, Veränderungen; Grenzen unsicher/angeschnitten kennzeichnen |
| `observations` | benannte Spalten, kompakte Zeilen und Sicherheitsangaben; identische Zeilenanzahl |
| `open_questions` | lokale Lücken, Widersprüche und alternative Deutungen |
| `suitability` | begründete Prognose, keine Garantie |

`observations.rows`: `[time_s, provisional_group, subdivision_index, candidates]`. Gruppen sind 1-basiert, Unterteilungen 0-basiert. Audio-Kandidat: `[pitch_midi, spectral_strength]`; MIDI-Kandidat: `[pitch_midi, velocity, offset_s]`. Diese Unterschiede stehen im jeweiligen `candidate_columns`-Feld. Gruppierungsraster ist eine Hypothese; außerhalb eines Rasters dürfen künftig eigenständige Zeitgruppen ergänzt werden, nicht zwangseinrasten.

`observations.confidence`: je Zeile `[pitch_confidence, rhythm_confidence, reason]`. Eine Spektralmessung darf mathematisch exakt gespeichert und musikalisch trotzdem unsicher sein.

Metrische Hypothese:

```
{"id":"m1","status":"hypothesis","meter":[6,8],
 "pulse_duration_s":[89,500],"pulse_duration_q":[1,4],
 "tempo_reference_q":[1,1],"tempo_per_minute":[7500,89]}
```

Das Beispiel bedeutet 0,178 Sekunden pro kleinem Puls, interpretiert als Sechzehntel, Vierteltempo exakt **7500/89**. Normale Befundfelder dürfen diese Deutung offenlassen; sie ist kein Auftrag zur Ausgabe im 6/8-Takt.

Verbindliche Konsistenzgleichung für jede gewählte Hypothese:

`pulse_duration_s = 60 × pulse_duration_q / (tempo_per_minute × tempo_reference_q)`.

Bei 0,178 s pro Sechzehntel: Viertel=7500/89≈84,269663 oder punktierte Viertel=5000/89≈56,179775. **Nicht** punktierte Viertel=84 und nicht Viertel=126. Tempoanzeigen dürfen gerundet sein; Berechnung arbeitet mit exakten Werten bzw. dokumentierter MIDI-Rundung.

Mehrere Hypothesen erhalten eigene IDs und Sicherheiten. Taktanzahl bleibt abhängig davon vorläufig. Sekundenvorlauf und Ausschnittgrenzen bleiben als Quellbefund erhalten; Entfernen beim Komponieren wird als Entscheidung protokolliert.

## 4. Vertrag B – Composition Plan (Ausgabevertrag)

Pflichtinhalt: `format=MusicCraft-Composition-Plan`, `version=0.2`, Plan-ID/Revision, Input-ID/Revision/SHA256, Kompositionsauftrag, gewählte metrische Hypothese oder begründete neue Interpretation, Stimmen, Takte, Noten/Pausen, Tempomap und Entscheidungen.

- Alle Noten erhalten `id`, `voice_id`, `staff`, `pitch_midi`, `onset_q`, `duration_q`; Notenwerte positiv. Gleichzeitige unterschiedliche Tonhöhen explizit als eigene Noten. Pausen ausdrücklich und ohne Tonhöhe.
- Takte: Beginn/Länge/Taktart; reguläre Länge=`numerator × 4 / denominator`. Auftakt/angeschnittene Takte explizit abweichend deklarieren.
- Stimmen müssen Takte einschließlich Pausen konsistent füllen; Akkordtöne zählen die Dauer nicht mehrfach. Taktübergreifende Noten im Score mit Bindungen teilen, beim Vergleich wieder zusammenführen.
- Tempomap: Position, positiver BPM-Wert und expliziter Bezugsnotenwert in `_q`. Keine unbeschriftete BPM-Zahl. Tempowechsel und Rubato dürfen nicht durch pauschales Tempo ersetzt werden, ohne dies zu begründen.
- Gestaltung optional/ungeklärt lassen, bis entschieden; jede ergänzte Note und aufgelöste Unsicherheit über `decision_id` zum Analysebefund zuordnen. Neue Noten nicht als erkannte Originaltöne ausgeben.
- Spielzeiten separat: `performance_onset_s` und `performance_duration_s` dürfen notierte Zeiten expressiv verändern. Dann explizite Zuordnung pro Noten-ID. MIDI gegen Performance vergleichen, MusicXML gegen Score; kein falscher Anspruch auf identische Dauern bei bewusstem Gate/Artikulation.

## 5. Export- und Prüfvertrag

1. **MIDI:** PPQ explizit. `ticks = duration_q × PPQ`; ausreichende Auflösung wählen. `microseconds_per_quarter = 60000000 / (BPM × reference_q)`. Toleranz für SMF-Tempo-Rundung und Tickauflösung numerisch dokumentieren.
2. **MusicXML:** `divisions` zählt Einheiten je Viertelnote. `duration = duration_q × divisions`. Sechzehntel brauchen bei divisions=480 den Wert 120. divisions=2 kann eine gewöhnliche Sechzehntel nicht ganzzahlig darstellen. Passende Auflösung wählen, niemals Werte still runden.
3. Numerische Dauer muss `type`, Punktierungen und Tuplet-Verhältnis entsprechen. Punktierte Halbe=3 Viertel, bei divisions=480 also1440; eine Achteltriole=160. Notationsmetronom und `sound tempo` müssen denselben Viertelpuls ausdrücken; `sound tempo` ist Viertel pro Minute.
4. Takt-/Stimmzeitachsen über `backup`, `forward`, `chord` korrekt rekonstruieren. In 6/8: 3 Viertel; zwölf Sechzehntel füllen genau einen Takt. Die Angabe 12 bei divisions=2 füllt dagegen sechs Viertel und ist abzulehnen.
5. Unabhängig wieder einlesen: Notenanzahl, Tonhöhen, Einsatzzeiten, Dauern, Tempo, Stimmen/Systeme und Taktfüllung prüfen. Keine offenen Noten oder neu eingeführten unbeabsichtigten Überlagerungen. Quelltreue zusätzlich musikalisch beurteilen.
6. Status pro Prüfung `passed`, `failed` oder `not_run`, Werkzeug/Version, gemessene Werte und Toleranz protokollieren. Ohne tatsächliche Ausführung keine Aussage „exakt geprüft“. Parserprüfung ersetzt weder reale Notensatz-/Sichtprüfung noch Hörvergleich.
7. Fehlende Angaben des Komponisten nicht durch den Exporter musikalisch erraten. Fehler melden oder eindeutig mechanische Korrektur protokollieren; keine unbemerkte Neukomposition.

## 6. Umfang dieses Schritts

Die beiden bestehenden privaten Pilotübergaben wurden konservativ in0.2 überführt; alte Dateien bleiben erhalten. Keine neuen Erkennungsbefunde hinzugefügt, keine Tonhöhen „repariert“. Einheiten/Deutungen explizit gemacht. Getestet werden Umrechnungsregeln einschließlich der aus dem Gemini-Text erkennbaren Fehler, keine behauptete Ausführung von Geminis Originalcode. Produktionsschema, Converter und UI-Integration folgen separat. Umfangreiche Kompositionspläne sind kein Analyseauftrag.
