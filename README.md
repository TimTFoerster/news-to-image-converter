
# Abschlussprojekt Gestaltungsgrundlagen
- Hochschule München
- Informatik & Design
- Wintersemester 2025/26
- Tim Förster

## Thema
### Verzerrung von Personen des öffentlichen Lebens
Von der scheinbaren Stabilität öffentlicher Figuren zur offensichtlichen Labilität durch die Verbildlichung von Nachrichtenartikeln. Die Bilder werden durch unterschiedlich eingefärbten Artikeltext dargestellt und verzerren die Außenwirkung öffentlicher Personen.

## Funktionsweise
Das Programm lädt über einen RSS Feed aktuelle Nachrichten von tagesschau.de und erstellt aus vorher ausgesuchten Bildern und dem Nachrichtentext ein zum Artikel passendes Bild in der Konsole von VS Code. Auf die gleiche Art wird dann ein zweites Bild dargestellt, diesmal in der Satire-Version.
In `main.py` befinden sich das Hauptprogramm.
In `colors.py` finden sich Konstanten und Dictionaries, die die Farben festlegen. In der Konsole können nur acht Farben dargestellt werden, deswegen werden die Bilder auf diese Farben reduziert.
In `image_selection.py` befinden sich Dictionaries mit den Schlüsselwörten, die entscheiden welches Bild für einen Artikel verwendet wird, sowie die Dateinamen der Bilder.

## Ausführung

1) Projekt Ordner in VS Code öffnen
2) `uv sync` im Terminal ausführen um die Abhängigkeiten zu installieren
3) `uv run main.py` im Terminal ausführen
4) Programm läuft in Endlosschleife. Abbruch mit Strg+C oder Konsole schließen

Hinweis: Um die Bilder besser darzustellen, in den Einstellungen "terminal font size" suchen und Schriftgröße auf 8 oder 6 stellen (Standard ist 12)

# International

Takes latest articles from tagesschau.de and turns them into images made of text displaying a satire character connected to people mentioned in the article.

Set Terminal/Console Font Size to 10 or 8 for best effect.

<img width="1139" height="651" alt="donald" src="https://github.com/user-attachments/assets/8fdbe185-9092-4e25-9f0f-4bcd4d2a2578" />