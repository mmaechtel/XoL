## Wine unter Debian 12 installieren – zwei Wege

[Wine](../glossary.md#wine-wine-is-not-an-emulator) erlaubt das Ausführen von Windows-Programmen unter Linux. Hier sind zwei Möglichkeiten, Wine auf Debian 12 zu installieren.

### 1. Installation über die Standard-Debian-Paketquellen
Zuerst das System aktualisieren:
```bash
sudo apt update && sudo apt upgrade -y
```

Dann Wine installieren:
```bash
sudo apt install wine
```

Die Installation prüfen:
```bash
wine --version
```

Das war’s – die Debian-Version ist schnell eingerichtet, aber möglicherweise nicht die neueste.

### 2. Installation über das WineHQ-Repository
Für eine aktuellere Version die 32-Bit-Architektur aktivieren und das Repository einbinden:
```bash
sudo dpkg --add-architecture i386
sudo apt update
sudo mkdir -pm755 /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources
sudo apt update
```

Wine installieren:
```bash
sudo apt install --install-recommends winehq-stable
```

Version überprüfen:
```bash
wine --version
```

Optional mit `winecfg` konfigurieren. Diese Variante bietet die neueste stabile Wine-Version.

### Fazit
Die Debian-Variante ist einfacher, WineHQ aktueller. Beide lassen sich leicht einrichten, je nach Bedarf.


## 3. Winetricks hinzufügen

Winetricks ist ein Hilfsskript, um zusätzliche Bibliotheken und Einstellungen für Wine zu installieren. So geht’s:

```bash
sudo apt install winetricks
```

Nach der Installation kann Winetricks genutzt werden, z. B. um DLLs oder Schriftarten hinzuzufügen:

```bash
winetricks dlls
```

Oder eine grafische Oberfläche starten:

```bash
winetricks --gui
```

Winetricks erleichtert die Feinabstimmung und erhöht die Kompatibilität mit manchen Windows-Anwendungen.


## 4. Installation der 32-Bit Version

Für manche ältere Windows-Programme wird die 32-Bit Version von Wine benötigt. So installieren Sie sie:

**32-Bit Architektur aktivieren und Wine32 installieren**

- Führen Sie folgenden Befehl aus, der die 32-Bit Architektur aktiviert, die Paketquellen aktualisiert und Wine32 installiert:
  ```bash
  sudo dpkg --add-architecture i386 && sudo apt-get update && sudo apt-get install wine32:i386
  ```

Alternativ können Sie die Schritte auch einzeln ausführen:
```bash
# 32-Bit Architektur aktivieren
sudo dpkg --add-architecture i386

# Paketquellen aktualisieren
sudo apt-get update

# Wine32 installieren
sudo apt-get install wine32:i386
```

Nach der Installation können Sie auch 32-Bit Windows-Programme ausführen. Dies ist besonders nützlich für ältere Software oder Programme, die keine 64-Bit Version haben.

