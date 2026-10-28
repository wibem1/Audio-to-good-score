# Projektstand – Audio to Good Score

**Stand:** 2026-10-28  
**Phase:** Konzept/Initialisierung, noch keine Implementierung und keine getestete App.  
**Repository:** `wibem1/Audio-to-Good-Score`  
**Produktname:** Audio to Good Score  
**Zielversion:** 0.1 (**geplant**, nicht freigegeben).

## Verbindliches Ziel
Web-App zur musikalisch überzeugenden Transkription und Rekonstruktion aus (a) Audio allein, (b) Audio + MIDI, (c) MIDI allein, mit gut klingendem MIDI- und lesbarem MusicXML-Export. Primär Klaviersolo. Standard-Modus **Musikalisch ausgewogen**: musikalischen Charakter erhalten, ausgewählte Fehler sinnvoll korrigieren, keine pauschale Neuerfindung.

## Gesicherte Entscheidungen
- Alle drei Eingangswege gehören zum Umfang V0.1.
- Technische Validität allein bedeutet keine musikalische Qualität; A/B-Hörvergleich und echte Partiturprüfung nötig.
- Originaldaten bleiben unverändert, Änderungen sind begründet und reversibel.
- Expressive MIDI-Performance ist getrennt von lesbarer MusicXML-Notation.
- „Graziler Tanz“ dient als Referenzfall, Testdateien sind nicht automatisch im Repository vorhanden.
- Detailliertes Konzept und Abnahmekriterien: `PFLICHTENHEFT_V0.1.md`.

## Nachgewiesene Funktionen
**Keine.** Bisher wurden keine App-Funktionen implementiert, gebaut oder getestet.

## Aktuelle Risiken/Blocker
- Modell-/Lizenz- und Ressourcenprüfung für polyphone Klaviertranskription steht aus.
- Musikalische Qualität kann nicht durch XML-Validierung oder MIDI-Eventzählung garantiert werden.
- Referenzaudio und geeignete Test-MIDI müssen für reproduzierbare Tests bereitgestellt und rechtmäßig versioniert werden.
- Projektarchitektur und Deployment noch nicht festgelegt.

## Nächster einzelner Entwicklungsschritt
Architektur und Bibliotheken auf Lizenz, Runtime und Machbarkeit für Import/Alignment/A-B-Player prüfen; danach kleinsten isolierten Prototyp für Meilenstein 1 bauen und tatsächlich testen.

## Übergabe
Vor Fortsetzung globale Entwicklungsstandards lesen, danach `AGENTS.md`, diese Datei, `TODO.md`, Pflichtenheft und relevanten Code. Status immer anhand GitHub prüfen. Keine unbestätigten Erfolgsaussagen.
