# Pflichtenheft – MusicCraft App, Zielversion 0.1

**Stand:** 29.10.2026. **Status:** verbindliche Anforderungsbasis. Neuausrichtung mit zwei Modulen beschlossen, aber noch nicht implementiert (Abschnitt 12). Meilenstein 1 und der lokale Audio-only-Kandidatenweg aus Meilenstein 2 technisch geprüft, musikalische Abnahme offen; Einzelstatus siehe `PROJECT_STATE.md`. V0.1 ist nicht freigegeben.  
**Plattform:** Web-App, nutzbar auf Windows/macOS/Tablets.  
**Zielgruppe:** Musiker, die aus Audio oder fehlerhaften Transkriptionen klanglich überzeugende MIDI und lesbare MusicXML erzeugen wollen.  
**Startumfang:** Soloklavier. **Referenz:** „Graziler Tanz“ (Audio + erste MIDI, nur wenn Testdateien verfügbar).  
**Standardmodus:** **Musikalisch ausgewogen**.

## 1. Produktziel
MusicCraft App verbindet die eigenständig nutzbaren Module **Analyse** und **Komposition**. Sie analysiert Audio, MIDI oder beides, rekonstruiert musikalisch fehlerhaftes Material und ermöglicht eigenständige neue Komposition aus Motiven oder Vorgaben. Audio to Good Score ist ein Anwendungsfall, nicht mehr die Begrenzung des Produkts. Ausgangsumfang und erste Validierung bleiben Soloklavier; weitere Besetzungen sind eine spätere Erweiterung.

Nicht die maximale Zahl exakt übertragener Noten entscheidet, sondern eine musikalisch schlüssige Interpretation: tragende Melodie, motivische Wiedererkennbarkeit, harmonischer Sinn, rhythmischer Fluss, natürlicher Ausdruck, nachvollziehbare Form und spielbare, lesbare Klaviernotation. Änderungen dürfen maßvoll vom Original abweichen, wenn sie musikalisch helfen; intakte Abschnitte bleiben unverändert.

## 2. Gleichrangige Eingangspfade
- **A – Nur Audio** (MP3, WAV): polyphone Klaviertranskription, musikalische Analyse und Rekonstruktion; Vergleich zwischen Audio und renderbarer MIDI.
- **B – Audio + MIDI**: vorhandene Transkription durch zeitliche Ausrichtung und Audiovergleich gezielt verbessern; nicht grundlos neu transkribieren.
- **C – Nur MIDI**: musikalische Strukturanalyse, Reparatur, Klaviernotation; ohne Audio sind Tonhöhenfehler nicht sicher verifizierbar und müssen als unsicher gekennzeichnet werden.

Eine vorhandene MIDI ist eine zusätzliche, möglicherweise fehlerhafte Quelle. Bei Audio+MIDI bleibt Audio die maßgebliche klangliche Referenz; Widersprüche werden angezeigt, nicht still aufgelöst. MIDI-only ist vollwertig, erlaubt aber keine sichere Aussage über eine nicht vorliegende Originalaufnahme. Zusätzlich gibt es freie Komposition aus Motiv oder Vorgaben ohne importierte Vorlage und ohne verpflichtende Quellenanalyse.

Alle Pfade können über kontrollierte, versionierte Bearbeitungen zu MIDI- und MusicXML-Export führen. Audio-only ist ausdrücklich Kernumfang von 0.1, nicht eine spätere Option.

## 3. Qualitätsprioritäten (heuristisch, keine erfundenen Messwerte)
- Melodie und motivische Substanz: **25 %**
- Rhythmischer Fluss und charakteristischer Puls: **25 %**
- Harmonik/Bass/Stimmenführung: **20 %**
- Ausdruck/Charakter/Entwicklung: **15 %**
- Klaviersatz/Spielbarkeit: **10 %**
- Schonender Umgang mit intakten Stellen/Originalnähe: **5 %**

Diese Gewichtungen priorisieren Reviews; es gibt noch kein kalibriertes automatisches Prozent-Rating. Uneindeutige Stellen kennzeichnen statt ungeprüft zu verändern.

## 4. Funktionale Anforderungen
| ID | Verpflichtende Funktion | Abnahmehinweis |
|---|---|---|
| F01 | Audioimport MP3/WAV | Audio vollständig abspielbar |
| F02 | MIDI-Import (SMF) | Noten, Tempo, Pedal, Dynamik und Spuren möglichst erhalten |
| F03 | Audio-MIDI-Alignment, bei Bedarf manuell justierbar | Synchronisierte Abschnittsnavigation |
| F04 | A/B/C-Player: Audio, Ausgangs-MIDI, Bearbeitung | Hörvergleich gleicher Passage |
| F05 | Pianorolle mit Markierung | Noten und Reparaturbereiche sichtbar |
| F06 | Fehlerdiagnose | verdächtige Timing-/Tonhöhen-/Längen-/Stimmstellen nachvollziehbar |
| F07 | KI-gestützte musikalische Analyse | Melodie, Motivik, Harmonik, Rhythmus mit Unsicherheit |
| F08 | Selektive KI-Korrektur | Nur gewählter Abschnitt geändert, Begründung dokumentiert |
| F09 | Änderungsvergleich, Undo/Redo | Vollständige Reversibilität |
| F10 | MIDI-Export | Freigegebene Performance-Zeiten/Velocity/Pedal respektiert |
| F11 | MusicXML-Export | zweisystemige Klaviernotation mit Stimmen/Pausen/Bögen/Balken |
| F12 | Diagnoseexport | Quellen, Nutzeranweisungen, Modellparameter/Kosten, Änderungen, Validierungen |
| F13 | Projekt-/Versionenspeicherung | Ursprünge unverändert und abrufbar |
| F14 | Audio-only-Transkriptionspfad | Ohne vorhandene MIDI entsteht überprüfbarer MIDI-Kandidat |

## 5. Bearbeitungsregeln
- **Zwei Zeitdarstellungen:** expressive Spielzeiten im Performance-Modell; quantisierte, metrisch konsistente Zeitwerte nur im Score-Modell. Keine rückwirkende Zwangsquantisierung des Hör-MIDI.
- **Tempo:** eine dichte importierte Tempokurve nicht blind löschen; zuerst Ereignisse und absolute Zeit überprüfen. Notations-Tempozeichen separat sparsam ableiten.
- **Musikalische Reparatur:** Kontext über Nachbartakte, Bass/Harmonie, Motive, Stimmen und soweit vorhanden Audiosignal heranziehen. Für jede Änderung Hypothese, Vorher/Nachher und Unsicherheit speichern.
- **Sicherheit:** Original unverändert, atomare Änderungen, Undo/Redo; bei zweifelhaften Änderungen Nutzerentscheidung.
- **Unterschied MIDI vs. Notation:** Die Partitur darf lesbare Rhythmen verwenden, ohne die expressive Wiedergabe zu beeinträchtigen.
- **Keine stillen KI-Neukompositionen:** Umfang und Identität jeder Änderung müssen nachvollziehbar sein.

## 6. Qualitätskontrolle und Freigabe
1. **Technisch:** gültige Dateien, stabile Zeit-/Notenereignisse, unveränderte Originale; MusicXML wird erneut eingelesen; Takt-/Stimmkonsistenz.
2. **Musikalisch:** Motiv-/Melodieführung, Harmonik, lokaler Puls, Ausreißer, Spielbarkeit; Bearbeitung gegen Vorversion und ggf. Referenzaudio prüfen.
3. **Perzeptiv:** A/B-Hörvergleich synchronisierter Passagen, kein künstliches Holpern oder unerklärte Verluste; menschliche Hörfreigabe, solange automatisches Maß nicht validiert.
4. **Notation:** importierte Partitur in Dorico/MuseScore visuell prüfen, inklusive realem Zweihandsatz.
5. **Transparenz:** Status unterscheiden: geplant / implementiert / technisch geprüft / musikalisch geprüft / vom Nutzer bestätigt. Technischer Pass ist keine musikalische Abnahme.

## 7. Konkrete Abnahmetests
| ID | Test / Erfolgsbedingung |
|---|---|
| A01 | Audio und MIDI laden, korrekt zuordnen und ausrichten |
| A02 | Originale bleiben unverändert, sind wieder abrufbar |
| A03 | Verdachtsstellen im musikalischen Kontext darstellen |
| A04 | Markierte Passage bearbeitbar; Nachbarpassagen bleiben unverändert |
| A05 | Originalaudio, Ausgangs-MIDI und Bearbeitung abschnittsweise vergleichbar |
| A06 | Änderungen vollständig rückgängig und wiederherstellbar |
| A07 | Keine neu eingeführten Timing-Störungen durch Tempo-/Quantisierungsänderung |
| A08 | MIDI-Export spielt genehmigten Verlauf ab |
| A09 | MusicXML wird in Dorico und MuseScore geöffnet; lesbar und korrekt strukturiert |
| A10 | Diagnose enthält Eingaben, Anweisungen, Begründungen und Prüfergebnisse |
| A11 | Audio-only: aus einer MP3/WAV wird unabhängig von vorhandener MIDI ein Kandidat erstellt, angehört und überarbeitet |
| A12 | Ergebnis nur nach tatsächlicher Prüfung entsprechend gekennzeichnet; fehlende Prüfung klar benannt |

## 8. Technische Optionen, noch nicht entschieden
Web-Frontend React/TypeScript; Audio Web Audio API; MIDI z.B. mido/pretty_midi; Audioanalyse z.B. librosa; Transkriptionsmodelle (Klavier spezialisiert, Basic Pitch als Vergleich); Server FastAPI; Score-Modell/music21/Partitura; MusicXML-Rendering Verovio. Lizenz-/Performance-/Deployment-Eignung vor Implementierung überprüfen.

## 9. Bisherige technische Meilensteine (historische Reihenfolge)
**Meilenstein 1:** Audio- und MIDI-Import, Zeitachsen-Vergleich, Abschnittsmarkierung, nicht-destruktive manuelle Reparatur, Undo, MIDI-Export.  
**Meilenstein 2:** Audio-only-Transkription integriert und anhand Hörvergleich überprüfbar.  
**Meilenstein 3:** KI-gestützte selektive Reparatur mit Diagnose und Versionsvergleich.  
**Meilenstein 4:** MusicXML-Export und reale Notationsprüfung.

Die Reihenfolge beschreibt den bisherigen Prototyp, nicht die nächste Umsetzung der MusicCraft-Module. Nächste Priorität: prüfbares Analysebericht-Modell und einfache Modulansicht; danach echte musikalische Analyse und explizit beauftragte Komposition. Alle bisherigen Qualitätslücken bleiben offen; keine pauschale Freigabe vor den Abnahmen.

## 10. Ausgeschlossen in V0.1
Orchester-/Mehrinstrumenten-Arrangement, perfekter Notenrekonstruktionsanspruch, eigener Modell-Trainingsprozess und vollständiger Noteneditor. Eigenständige neue Komposition ist dagegen ausdrücklich Produktziel; umfassende Änderungen oder Neukompositionen ohne Nutzerauftrag sind ausgeschlossen.

## 11. Versions-/Kostenregeln
Keine als funktionsfähig veröffentlichte V0.1 ohne tatsächliche Kernprüfungen. Kostenpflichtige Modellaufrufe nur nachvollziehbar, mit Limits und Diagnose. Nach jedem nachgewiesenen Schritt PROJECT_STATE aktualisieren. Der aktuelle nachgewiesene Umsetzungsstand steht verbindlich in `PROJECT_STATE.md`; dies ist keine Freigabe der Gesamtversion V0.1.



## 12. Verbindliche Modulspezifikation MusicCraft App

Beschlossen am 29.10.2026. Die folgenden Anforderungen erweitern F07/F08 und ersetzen eine Beschränkung auf technische Transkription oder Einzelnotenreparatur. Sie sind **geplant**, nicht durch frühere technische Tests abgenommen. F01–F14 und A01–A12 bleiben als technische Grundlage und Schutzregeln erhalten; Basic Pitch liefert Hinweise, keine musikalische Komposition.

### 12.1 Modul Analyse

Eigenständig benutzbar und speicherbar, ohne Kompositionsauftrag. Eingänge: Audio allein, MIDI allein oder Audio mit MIDI. Die KI untersucht die Quelle so genau wie möglich, um musikalische Identität und Veränderungen zu erfassen. Bei MIDI-only technische Defekte, musikalische Auffälligkeiten und mehrdeutige Intention unterscheiden. Ungewöhnliche Töne oder Rhythmen sind kein Fehlernachweis. Keine erfundene Rekonstruktion einer unbekannten Originalaufnahme.

Verbindlicher Kriterienkatalog:

| Bereich | Geforderter Befund |
|---|---|
| Besetzung | Instrumente, Stimmenzahl, solistische/mehrstimmige Anlage; MIDI-Programmnummer von tatsächlichem Instrument unterscheiden |
| Tonart/Tonalität | Grundton, Dur/Moll oder andere tonale Ordnung, lokale Zentren und Modulationen, alternative Deutungen |
| Taktart | Metrum, Schwerpunkte, Auftakt, Taktwechsel und Taktgrenzen |
| Tempo | Grundtempo mit Bezugsnotenwert, lokale Veränderungen, Rubato, Ritardando/Accelerando; Speichertempo von erkanntem musikalischem Puls unterscheiden |
| Taktanzahl | Gesamtzahl und Anzahl je Abschnitt; Auftakt, unvollständige und angeschnittene Takte ausdrücklich kennzeichnen |
| Form/Phrasen | Abschnitte, Phrasenlängen, Wiederholungen, Varianten, Übergänge und Abschlüsse |
| Musikstil/Charakter | Beschreibbare Stilmerkmale, mögliche Gattung, Charakter und Bewegungsart; keine unbegründete Komponistenzuschreibung |
| Melodieführung | Führende Stimme, Register, konkrete Anker-/Spitzentöne soweit erkennbar, Bewegungsrichtung, Schritte/Sprünge, Höhepunkte und Phrasenenden |
| Motive/Veränderungen | Ton-/Rhythmusmotive; Wiederholung, Versetzung, Umkehrung, Verkürzung/Erweiterung; für jede Phrase: was bleibt, was verändert sich? |
| Begleitung | Figur, Akkordlagen, Rhythmus, Register, Dichte, Varianten und Verhältnis zur Melodie |
| Bassführung | Basstöne, Verlauf, Halte-/Orgelpunkte, Sprünge und harmonischer Bezug |
| Harmonik | Akkorde mit Wechselzeitpunkten, harmonischer Rhythmus, Kadenzen, Spannung/Auflösung und Dissonanzen |
| Rhythmik | Charakteristische Werte/Pausen, Synkopen, Punktierungen, Triolen und andere Unterteilungen, Unterschiede zwischen Stimmen |
| Stimmenverhältnis | Gegenstimmen, Dialoge, Einsätze, Unabhängigkeit und Rollenwechsel |
| Artikulation/Verzierungen | Legato/Staccato, Akzente, Vorschläge, Triller und sonstige Verzierungen |
| Dynamik/Klanggestaltung | Verlauf, Stimmenbalance, Steigerungen/Rücknahmen, Pedal; Nachhall, gehaltene Töne und Pedal nicht ungeprüft gleichsetzen |

Jedes Kriterium erhält **Befund, Geltungsbereich, Sicherheit, kurze Begründung und offene Alternativen**. Befunde sind Quelle/Messung, musikalische Deutung oder Nutzerhinweis zuzuordnen. Ein Kriterium darf als nicht bestimmbar ausgewiesen werden; kein Zwang, eine Antwort zu erfinden.

Sicherheitsstufen:

- **Hoch:** klare, übereinstimmende Hinweise; Ergebnis bei Gegenprüfung stabil.
- **Mittel:** plausible Deutung mit relevanten Mehrdeutigkeiten.
- **Gering:** schwache oder widersprüchliche Hinweise; starke Abhängigkeit von Annahmen.
- **Nicht bestimmbar:** derzeit keine belastbare Aussage möglich.

Dies sind begründete Einschätzungen, keine kalibrierten Wahrscheinlichkeiten. Keine unvalidierten Prozentwerte oder Mittelwert-Gesamtnote. Hohe Sicherheit wird durch Analysebelege und Gegenprüfungen gestützt, nicht bloß durch Modellselbstauskunft. Richtung einer Melodie und genaue Tonhöhen separat beurteilen. Unsicherheiten weiterreichen: aus unsicherer Taktart/Grenze keine scheinbar sichere Taktanzahl ableiten.

### 12.2 Grafische Übersicht und einfache Bedienung

Standardanzeige: kurzes musikalisches Ergebnis, wichtigste Unsicherheiten und Empfehlung. Kriterien, Begründungen und Matrix sind aufklappbar; keine Pflicht, jeden Takt oder jede Note einzeln abzunehmen.

Anklickbare Taktfelder plus Matrix **Kriterien × Takte**: Grün/✓ hoch, Gelb/~ mittel, Rot/? gering, Grau/– nicht bestimmbar. Noch nicht analysiert als eigener Bearbeitungsstatus beschriften, nicht als schlechte Erkennung. Farben stets mit Symbol/Text ergänzen. Taktzusammenfassung muss kritische Unsicherheiten sichtbar halten; keine grüne Gesamtbewertung durch Mittelung über eine unklare Melodie. Details zeigen Sicherheit je Kriterium und mögliche Deutungen.

Unsichere Taktgrenzen gestrichelt/vorläufig darstellen; wenn keine belastbare Einteilung besteht, Zeitabschnitte statt erfundener Taktnummern verwenden. Bei MIDI dieselben Abschnitte direkt abspielen. Antippen öffnet passende Quelle, Befunde und einfache Texteingabe, z.B. „Hier steigt die Melodie von unten auf“. Nutzerkorrekturen mit Herkunft speichern, davon abhängige Befunde überprüfen; sie sind kein unabhängiger Erkennungsnachweis.

### 12.3 Eignung und erwartbare Vorlagennähe

Vor einem Auftrag beurteilt die KI, ob Imitation sinnvoll erscheint und welche Nähe voraussichtlich erreichbar ist:

| Prognose | Begründete Erwartung |
|---|---|
| Vorlagennah | Prägende Melodie, Rhythmik, Harmonik und Begleitung weitgehend übertragbar |
| Musikalisch ähnlich | Charakter und wesentliche Ideen erkennbar, mehrere Details zu ergänzen |
| Freie Annäherung | Nur Teile belastbar erkannt; größere kompositorische Entscheidungen erforderlich |
| Derzeit wenig sinnvoll | Zu viele prägende Merkmale offen; bessere Quelle, andere oder kürzere Passage vorschlagen |

Nähe ausdrücklich je relevantem Bereich begründen; sichere Harmonie ersetzt keine unklare Melodie. Prognose ist keine Erfolgsgarantie und ohne Originalaudio bei MIDI-only keine Aussage über unbekannte Klangtreue. Bericht benennt zu bewahrende Merkmale, offene Schlüsselfragen und voraussichtlich zu ergänzende Details. Schwache Prognose ist eine Entscheidungshilfe, keine automatische Sperre; eine bewusst gewählte freie Annäherung bleibt möglich.

### 12.4 Modul Komposition

Drei Aufgaben: **Nachkomposition/Imitation**, **gezielte Überarbeitung**, **neue Komposition aus Motiv oder Vorgaben**. Standard „Musikalisch ausgewogen“; Nähe/Änderungsumfang bewusst wählen. Freie Komposition ohne Vorlage benötigt keine vorangestellte Audio-/MIDI-Analyse.

Vorlagenbezogener Ablauf: Quelle laden → analysieren → Bericht und Prognose zeigen → optional Hinweise/erneute lokale Analyse → **ausdrücklicher Auftrag des Anwenders** → komponieren → Original/Revision vergleichen. Keine automatische Generierung nach dem Laden oder Analysieren. Primäre Handlungen: „Imitation erstellen“, „Analyse ansehen“, „Andere Passage wählen“; bei MIDI entsprechend Quelle/Abschnitt. Keine kostenpflichtigen KI-Aufrufe ohne Zustimmung, auch nicht im Analysemodul. Vor bezahlter Beauftragung Kostenannahmen/Limit zeigen; Verbrauch diagnostizieren, keine unbeabsichtigten bezahlten Wiederholungen.

Übergabe zwischen Modulen: unveränderte Quellen mit Identität, gewählter Bereich und Kontext, versionierter Analysebericht, Sicherheit/Alternativen, Nutzerhinweise, zu bewahrende Merkmale und ausdrücklich erlaubte Ergänzungen/Änderungen. Quelle oder Analyse geändert: davon abhängige Prognose/Komposition als veraltet markieren; erneute Beauftragung erforderlich. Bestehende Ergebnisse erhalten, nicht löschen oder automatisch kostenpflichtig neu erzeugen.

Kompositorische Regeln: Analyse prägender Merkmale respektieren; jede Phrase eigenständig mit der Quelle abgleichen. Wiederholungen ebenso belegen wie Abweichungen. Unsicherheit nie still durch Fortsetzen eines vertrauten Musters füllen. Ergänzte Details als Interpretation kennzeichnen. Intakte Abschnitte bei selektiven Revisionen unverändert lassen. Original/Versionen bleiben abrufbar, Änderungen vergleichbar und reversibel; Einzelnotenbearbeitung ist optionales Expertenwerkzeug.

Ausgaben: abspielbare Fassung, MIDI und MusicXML, Analyse-/Änderungs-/Kostenbericht. Performance und lesbare Notation getrennt führen. Keine neuen rhythmischen Fehler durch Notationsvereinfachung; Taktfüllung, Einsätze, Dauern, Tempo, Ereignisverluste und Übergänge technisch prüfen, musikalische Qualität zusätzlich am Original beurteilen. Bei A/B möglichst gleicher Renderklang; abweichende Klangquellen offenlegen.

### 12.5 Neue Abnahmefälle (noch offen)

| ID | Erfolgsbedingung |
|---|---|
| MC01 | Audio-only, MIDI-only und Audio+MIDI liefern eigenständig nutzbare, speicherbare Analysen ohne Kompositionsstart |
| MC02 | Jeder Katalogbereich enthält Befund oder ausdrücklich fehlende Bestimmbarkeit, Bereich, begründete Sicherheit und ggf. Alternative |
| MC03 | Sicherheit je Takt/Kriterium sichtbar; unsichere Taktgrenzen führen zu vorläufigen Takten/Zeitabschnitten und abhängiger Taktanzahl |
| MC04 | Abweichende Schlussfigur wird eigenständig untersucht; Test verhindert ungeprüfte Wiederholung des vorigen Musters |
| MC05 | Kurzurteil mit Eignung/Vorlagennähe und Grenzen; Details optional, Quellabschnitt erreichbar und Nutzerhinweis ohne Noteneditierpflicht möglich |
| MC06 | Ohne ausdrücklichen Auftrag keine Nachkomposition; keine bezahlten Aufrufe ohne Zustimmung; Kosten/Abbrüche ohne automatische bezahlte Wiederholung nachvollziehbar |
| MC07 | Quelle/Analyse/Nutzerhinweise versioniert übergeben; Änderungen markieren abhängige Ergebnisse als veraltet, erhalten aber Vorversionen |
| MC08 | MIDI-only unterscheidet technische Fehler von ungewöhnlicher Musik; freie Komposition aus Vorgaben funktioniert ohne Vorlagenanalyse |
| MC09 | Selektive Revision erhält Nachbarabschnitte; Undo/Redo, Export und unabhängiger Ereignisvergleich zeigen keine neu eingeführten Rhythmusfehler |
| MC10 | Reale kurze Passage technisch sowie im menschlichen Hörvergleich beurteilt; tatsächliche Nähe mit Prognose verglichen, Notation in Zielprogrammen geprüft; keine Verallgemeinerung aus einem gelungenen Ausschnitt |

Technische Prototypen mit Beispieldaten sind kein Nachweis echter Erkennungsqualität. Eine musikalische Nutzerbestätigung gilt für die geprüfte Passage, nicht pauschal für das Modell oder alle Eingaben.
