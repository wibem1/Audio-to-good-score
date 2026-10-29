# MusicCraft App

Musik analysieren und komponieren: zwei eigenständige Module mit optionaler Übergabe von Analysebefunden an die Nachkomposition. Arbeitsmodus **Musikalisch ausgewogen**.

**Aktuelle technische Beta 0.1.0 Beta 1:** Browseroberfläche mit Audio-/MIDI-Import, Player und A/B-Vergleich, aufklappbarer Analyse, Chat, versionierten Kompositionsplänen, Undo/Redo, Partitur und geprüftem MIDI-/MusicXML-Export. Keine lokale Installation für die Web-App nötig.

[Benutzung, Architektur, Kosten und Grenzen](WEB_BETA.md) · [Projektstand](PROJECT_STATE.md) · [Übergabeformat und Kernprofil](protocol/IMPLEMENTATION_0.3.md).

**Die technische Beta ist keine musikalische Qualitätsfreigabe.** Die generative KI-Anbindung benötigt einen eigenen Gemini-Schlüssel und Zustimmung vor jedem Auftrag. Live-Modelltests und musikalische Abnahme stehen aus; während der Entwicklung wurden keine kostenpflichtigen KI-Aufrufe ausgeführt. Lokale Voranalyse ersetzt keine musikalische Deutung. Andere KIs können über Analyseexport und Kompositionsplan-Import beteiligt werden.

Der frühere Reparaturprototyp bleibt dokumentiert in [LEGACY_README.md](LEGACY_README.md). Seine Terminal-Anleitung gehört nicht zum Start der neuen gehosteten Web-App.
