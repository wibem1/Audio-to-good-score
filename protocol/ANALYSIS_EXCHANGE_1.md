# Analyseaustausch 1 – Ergänzungen statt Vollabschrift

Die dauerhafte Übergabe zwischen Analyse und Komposition bleibt **Analysis Handoff 0.3**. Neu ist der interne KI-Austausch `MusicCraft-Analysis-Interpretation`, Version `1`, mit eigenem JSON-Schema. Der Analyseauftrag verlangt keine vollständige Partitur und keine erneute Ausgabe aller Notenkandidaten.

1. Lokale Messbefunde bleiben unverändert im Projekt. Für die Anfrage werden Beobachtungen verlustfrei tabellarisch dargestellt: gemeinsame Standardwerte einmal, wiederholte Werte als Wörterbuchindizes, gleichförmige Tonkandidaten als Spaltenarrays. Originalsekunden bleiben exakt erhalten; fehlend und null bleiben unterscheidbar. Der Transport enthält eine explizite Dekodierregel.
2. Die KI erhält die ausgewählte Audiopassage (falls vorhanden), die kompakte Befundtabelle, Nutzerhinweise und das kleine Ausgabeschema. Pflichtkriterien: Tonalität, Metrum, Tempo/Bezugswert, Taktanzahl, Stil, Form, Melodieführung, Harmonik, Bass, Begleitung, Rhythmik und Ausdruck. Nicht erkennbare Kriterien müssen ausdrücklich unsicher bleiben. Kurzanalyse und detaillierte Befunde bleiben getrennt; keine erfundenen Prozentwerte.
3. Antwort: Kurzanalyse, begründete Kriterienbefunde, optionale musikalische Abschnitte, metrische Hypothesen, offene Fragen und Eignungsprognose. Höchstens 32 gezielte Beobachtungsergänzungen; keine erneute Volltabelle. `observation_updates=[]` bedeutet keine bestätigten Einzelkorrekturen, nicht automatische Bestätigung sämtlicher Detektortöne.
4. Jede Antwort verweist mit ID, Revision und kanonischer SHA-256 auf die genaue Grundlage. Der lokale Kern prüft Schema, Referenz, Pflichtkriterien, Quellen, vollständige Abschnittszuordnung, Abhängigkeiten und die Puls-/Tempo-Gleichung. Erst danach entsteht eine neue Analyse-Revision. Scheitert eine Prüfung, bleiben Ausgangsdaten unverändert.
5. Updates dürfen Kandidaten/Sicherheit/Begründung verfeinern; keine Messzeit oder Ereignis-ID ändern und keine unbekannten IDs einfügen. Neue Abschnitte müssen alle bestehenden Beobachtungen eindeutig zuordnen. Die Komposition bleibt ein eigener ausdrücklicher Auftrag. Menschliche Prüfung von Interpretation und Vorlagennähe bleibt erforderlich.

`musiccraft/analysis_exchange.py` implementiert Transport, Anfrage und atomare Zusammenführung; `web/analysis-flow.js` hält den Ablauf getrennt von der Oberfläche. Der gleiche kompakte, verlustfreie Kontext wird bei Analysegesprächen und vorlagenbezogenen Kompositionsaufträgen benutzt. Exportierte vollständige Analysen und Projekte bleiben kompatibel; Beta-1-Projekte werden in Beta 2 übernommen.

## Budget und Diagnose

Ausgabelimit wird nicht automatisch erhöht. Kein automatischer Folgeauftrag, keine Wiederholung und keine automatische Fortsetzung nach `MAX_TOKENS`. Ein Textumfang über 60.000 Zeichen wird vor Generierung gestoppt; dies ist eine technische Umfangsgrenze, keine Token- oder Geldgarantie. Das Ziel von 1500–3000 sichtbaren Ausgabetokens ist eine Promptvorgabe, keine gemessene Zusicherung. Details können durch einen gesondert gewählten kürzeren Abschnitt erneut analysiert werden; keine automatische kostenpflichtige Abschnittskette.

Jeder tatsächlich gestartete Aufruf protokolliert Modell, Auftrag, übergebenes Limit, Textzeichen, Anhanggröße, HTTP-/Abschlussstatus, Laufzeit sowie die vom Anbieter gemeldeten Eingabe-, Antwort-, Denk- und Gesamtzähler. Auch unvollständige Antworten und Abbrüche werden erfasst. Persistierung wird vor Rückgabe des Providerergebnisses versucht; fehlende Zähler bleiben unbekannt, niemals vermeintlich null. Diagnose ist ohne fertige Komposition verfügbar. Kein Schlüssel, Audioinhalt, Prompt oder Denkinhalt im Diagnoseprotokoll. Alte nicht protokollierte Verbräuche sind nicht rekonstruierbar.

## Prüfung und Grenzen

Messung der privaten 10-Sekunden-Voranalyse: zuvor 56.652 Zeichen allein für expandierte Befunde und Schema; jetzt 13.232 Zeichen für den **gesamten** neuen Analyseprompt einschließlich Anweisungen. 76,6 % weniger Zeichen, sämtliche 144 Beobachtungen erhalten. Keine Gleichsetzung mit Token- oder Kostenersparnis. Nutzerdatei nicht in das Repository übernommen; veröffentlicht werden nur aggregierte Größen.

Nachweise in `test-results/analysis-redesign/`. Providerreaktionen werden ohne Netzaufrufe simuliert; lokale Zusammenführung zusätzlich im echten Browser/Pyodide geprüft. Keine neue Behauptung über tatsächliche KI-Erkennungsqualität, Tokenverbrauch oder musikalische Abnahme. Kostenpflichtige Testaufrufe: null.

Offizielle Referenz zu getrennten Zählern: https://ai.google.dev/gemini-api/docs/generate-content/tokens ; gemeinsame Ausgabe-/Denkbegrenzung: https://ai.google.dev/gemini-api/docs/generate-content/thinking . Modellabhängiges Denken wird nicht ungeprüft umkonfiguriert.
