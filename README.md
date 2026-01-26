# P2P Bank

Jednoduchý školní/projektový „bankovní uzel“ implementovaný v Pythonu. Aplikace kombinuje **TCP server** pro obsluhu klientských požadavků a lehký **webový monitor** (Flask) pro průběžný dohled nad stavem a možnost řízeného vypnutí.

---

## Co aplikace dělá

- spouští **TCP server** (bankovní uzel), který přijímá klientská připojení a zpracovává příkazy,
- udržuje **perzistentní stav banky v souboru** (výchozí `bank_data.json`),
- současně spouští **webové rozhraní pro monitoring** (Flask) na `http://localhost:8080`, kde je vidět aktuální stav a je možné uzel bezpečně vypnout.

---

## Požadavky

- Python 3 (doporučeno 3.10+)
- závislosti:
  - **Flask** (web monitor)
  - **PyYAML** (načítání konfigurace z `config/config.yaml`)

---

## Rychlé spuštění (lokálně)

1) Naklonování repozitáře a přechod do složky projektu:
```bash
git clone https://github.com/maru-bor/p2p_bank.git
cd p2p_bank
```

2) vytvoření a aktivace virtuálního prostředí:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

3) Instalace závislostí:

```bash
pip install -r requirements.txt
```

4) Spuštění uzlu:
```bash
python main.py
```

---

## Jaké služby se spustí a kde je najdete

### 1) TCP server (bankovní uzel)
- port i další parametry se načítají z konfigurace `config/config.yaml`
- výchozí hodnoty:
  - host: `127.0.0.1`
  - port: `65525`

Konfigurační soubor: `config/config.yaml`  
Důležité položky:
- `bank.port` – port TCP serveru
- `storage.data_file` – cesta k souboru s uloženými daty (default `bank_data.json`)
- `logging.file` – cesta k log souboru (default `logs/bank_node.log`)
- `timeouts.*` – timeouty pro klienty a zpracování příkazů

### 2) Web monitor (Flask)
Po spuštění je dostupný na:
- `http://localhost:8080/`

Zobrazuje zejména:
- IP/identifikaci uzlu
- uptime
- počet klientů
- celkový objem prostředků (souhrnnou částku)

Součástí je i akce **Shutdown node**, která volá `POST /shutdown` a provede korektní ukončení uzlu.

---

## Provozní poznámky

- Pokud aplikace nemůže zapisovat logy do `logs/bank_node.log`, vytvořte složku `logs`:
```bash
mkdir -p logs
```

- Data banky se ukládají do souboru definovaného v `config/config.yaml` pod `storage.data_file` (standardně `bank_data.json`) v kořeni projektu.
## Použité zdroje
Níže jsou uvedeny odkazy na zdroje, které byly použity při tvorbě tohoto projektu.
- https://docs.python.org/3/howto/sockets.html
- https://docs.python.org/3/library/socket.html
- https://docs.python.org/3/library/logging.html
- https://realpython.com/python-sockets/
- https://refactoring.guru/design-patterns/command
- https://www.geeksforgeeks.org/system-design/registry-pattern/

Projekt také obsahuje znovu použitý kód z těchto předešlých projektů:
- https://github.com/maru-bor/library_management_system/blob/master/db/config_loader.py
- https://github.com/throw-away67/portfolio/blob/e39e2f5db7a140bc24f62d2430fdeac33b82d0c0/database_project/src/config.py
