# System-Tuning X-Plane 12 + AutoOrtho (Dino Fork)

System: Ryzen 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3× NVMe, Liquorix Kernel

## Problem

X-Plane + AutoOrtho streamen DDS-Tiles über FUSE. Jede Tile wird einmal gelesen, nie wieder.
Der Kernel cached trotzdem alles im Page Cache → 50+ GB toter Cache → Swap-Churn (17 GB Swap, 3 GB Swing/5 Min).

## Bereits umgesetzt

| Änderung | Datei | Vorher → Nachher |
|----------|-------|------------------|
| QEMU RAM | `virsh setmaxmem win11` | 12,5 GB → 5 GB |
| FUSE direct_io | `autoortho_fuse.py:222` | fehlt → `direct_io=True` |

Branch: `feature/direct-io-linux` in `autoortho4xplane`

## Optionen zum Testen

### Option A: direct_io allein (empfohlen als Startpunkt)

Nur `direct_io=True` + QEMU-Reduktion. AutoOrtho-Caches auf Original lassen (8 GB + 2 GB).

**Warum:** Eliminiert ~50 GB toten Page Cache. AutoOrtho's eigener 8-GB-Cache ist der einzige Cache, reicht aber für Streaming. Erwartung: Swap ≈ 0.

**Risiko:** Keins. Tiles wurden ohnehin nie aus dem Page Cache re-gelesen.

### Option B: min_free_kbytes erhöhen

```ini
# /etc/sysctl.d/90-liquorix.conf
vm.min_free_kbytes = 524288   # 512 MB statt 192 MB
```

**Warum:** Gibt kswapd mehr Vorlauf vor direct reclaim. Bei Szenerie-Bursts (gemessen: 3,4 GB/s über alle NVMe) werden schlagartig GB-weise Pages alloziert. Mit 192 MB Watermark gerät der Kernel in synchrones Reclaim → Mikroruckler. 512 MB = 0,5% von 96 GB.

**Wann:** Falls trotz Option A noch gelegentliche Stotterer beim Szenerie-Wechsel auftreten.

### Option C: vfs_cache_pressure erhöhen

```ini
vm.vfs_cache_pressure = 200   # statt 100
```

**Warum:** ZL19-Orthos von Disk (nicht FUSE) landen weiterhin im Page Cache. Höherer Wert → Kernel wirft alte Pages schneller weg.

**Wann:** Nur falls ZL19-Tiles den Page Cache merklich füllen (>10 GB). Mit 49 GB frei nach Option A vermutlich unnötig.

### Option D: swappiness weiter senken

```ini
vm.swappiness = 1   # statt 10
```

**Warum:** Kernel swapt quasi nur noch im absoluten Notfall, bevorzugt Page-Cache-Reclaim.

**Wann:** Nur falls nach Option A noch Swap-Aktivität messbar ist. Mit 49 GB frei sehr unwahrscheinlich.

### Option E: AutoOrtho-Caches vergrößern

```ini
# ~/.autoortho [cache]
cache_mem_limit = 12    # statt 8
```

**Warum:** Mit direct_io ist AutoOrtho's Cache der einzige Cache. Größer = weniger Tile-Rebuilds bei Kursänderungen. Bei 49 GB freiem RAM kein Problem.

**Wann:** Falls im Flug häufig Tiles neu gebaut werden müssen (sichtbar als kurze Blur-Phasen).

## Testreihenfolge

1. **Option A** — Fliegen, Monitoring laufen lassen, Swap beobachten
2. Falls Swap > 0: **Option D** dazu
3. Falls Stotterer bei Szenerie-Wechsel: **Option B** dazu
4. Falls ZL19-Areas langsam laden: **Option C** testen
5. Falls Tile-Rebuilds sichtbar: **Option E** hochdrehen

## Monitoring

```bash
python3 monitoring/sysmon.py                           # 20 Min, 100ms
SYSMON_DURATION=600 python3 monitoring/sysmon.py       # 10 Min
```

Rohdaten in `/tmp/sysmon_out/` (oder `SYSMON_OUTDIR` setzen).

Wichtigste Metriken zum Vergleich vorher/nachher:
- Swap Used (war 17 GB, Ziel: <1 GB)
- Page Cache / buff/cache (war 52 GB, Ziel: <10 GB)
- IOWait% (war 0,4-0,9%, Ziel: <0,3%)
- TLB Shootdowns (war 3700/s, sollte mit weniger Page Cache sinken)
