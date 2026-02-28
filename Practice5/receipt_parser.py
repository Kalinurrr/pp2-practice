import re
import json
from pathlib import Path

# ---------------- Regex patterns ----------------
MONEY_ANY = re.compile(r"\d[\d ]*,\d{2}")  # "154,00", "1 200,00", "18 009,00"
MONEY_LINE = re.compile(r"^\s*\d[\d ]*,\d{2}\s*$")

# qty x price line: "2,000 x 154,00"
QTY_X_PRICE = re.compile(r"^\s*(\d+,\d{3})\s*x\s*(\d[\d ]*,\d{2})\s*$", re.IGNORECASE)

# Item number line: "1."
ITEM_NO = re.compile(r"^\s*(\d+)\.\s*$")

# Date/time line example: "Время: 18.04.2019 11:13:58"
DT = re.compile(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})")

# Totals
TOTAL = re.compile(r"ИТОГО:\s*(\d[\d ]*,\d{2})")
VAT = re.compile(r"НДС.*?:\s*(\d[\d ]*,\d{2})")

# Payment method: "Банковская карта: 18 009,00"
PAYMENT = re.compile(r"^(Банковская карта|Наличные)\s*:\s*(\d[\d ]*,\d{2})\s*$", re.MULTILINE)

# Optional useful fields
CHECK_NO = re.compile(r"Чек\s*№\s*(\d+)")
BIN = re.compile(r"БИН\s*(\d+)")
BRANCH = re.compile(r"Филиал\s+(.+)")


# ---------------- Helpers ----------------
def parse_money(s: str) -> float:
    # "18 009,00" -> 18009.0
    return float(s.replace(" ", "").replace(",", "."))

def clean_line(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())

def read_text(filepath: str = "raw.txt") -> str:
    return Path(filepath).read_text(encoding="utf-8", errors="ignore")


# ---------------- Core parsing ----------------
def extract_all_prices(text: str) -> list[float]:
    return [parse_money(x) for x in MONEY_ANY.findall(text)]

def extract_datetime(text: str) -> dict:
    m = DT.search(text)
    return {"date": m.group(1), "time": m.group(2)} if m else {"date": None, "time": None}

def extract_payment(text: str) -> dict:
    m = PAYMENT.search(text)
    if not m:
        return {"method": None, "amount": None}
    return {"method": m.group(1), "amount": parse_money(m.group(2))}

def extract_total_printed(text: str) -> dict:
    mt = TOTAL.search(text)
    mv = VAT.search(text)
    return {
        "total_printed": parse_money(mt.group(1)) if mt else None,
        "vat_printed": parse_money(mv.group(1)) if mv else None
    }

def extract_header_fields(text: str) -> dict:
    return {
        "branch": (BRANCH.search(text).group(1).strip() if BRANCH.search(text) else None),
        "bin": (BIN.search(text).group(1) if BIN.search(text) else None),
        "check_number": (CHECK_NO.search(text).group(1) if CHECK_NO.search(text) else None),
    }

def parse_items(text: str) -> list[dict]:
    """
    Receipt item format usually:
      N.
      Product name (may span multiple lines)
      qty x unit_price
      line_total
      Стоимость
      line_total (repeated)
    We'll grab: name, qty, unit_price, line_total.
    """
    # keep non-empty lines (preserve order)
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]

    items = []
    i = 0
    while i < len(lines):
        m_no = ITEM_NO.match(lines[i])
        if not m_no:
            i += 1
            continue

        item_index = int(m_no.group(1))
        i += 1

        # collect name lines until qty x price
        name_parts = []
        while i < len(lines) and not QTY_X_PRICE.match(lines[i]):
            # stop if we suddenly hit totals section
            if re.match(r"^(Банковская карта|Наличные|ИТОГО|Фискальный признак|Время:)", lines[i]):
                break
            # sometimes there are empty lines (we removed them, but still safe)
            name_parts.append(clean_line(lines[i]))
            i += 1

        name = clean_line(" ".join([p for p in name_parts if p]))

        qty = unit_price = line_total = None

        # qty x price
        if i < len(lines):
            m_qp = QTY_X_PRICE.match(lines[i])
            if m_qp:
                qty = float(m_qp.group(1).replace(",", "."))
                unit_price = parse_money(m_qp.group(2))
                i += 1

        # first money line after qty x price is usually line total
        if i < len(lines) and MONEY_LINE.match(lines[i]):
            line_total = parse_money(lines[i])
            i += 1

        # skip optional "Стоимость" and repeated cost line
        if i < len(lines) and lines[i].startswith("Стоимость"):
            i += 1
            if i < len(lines) and MONEY_LINE.match(lines[i]):
                i += 1

        # Only add if looks like a real item name
        if name:
            items.append({
                "index": item_index,
                "name": name,
                "qty": qty,
                "unit_price": unit_price,
                "line_total": line_total
            })

    return items

def calculate_total_from_items(items: list[dict]) -> float:
    return round(sum(it["line_total"] for it in items if isinstance(it.get("line_total"), (int, float))), 2)


def parse_receipt(text: str) -> dict:
    header = extract_header_fields(text)
    dt = extract_datetime(text)
    payment = extract_payment(text)
    totals = extract_total_printed(text)

    items = parse_items(text)
    product_names = [it["name"] for it in items]
    all_prices = extract_all_prices(text)

    total_calc = calculate_total_from_items(items)

    return {
        "meta": header,
        "date_time": dt,
        "payment": payment,
        "totals": {
            **totals,
            "total_calculated_from_items": total_calc
        },
        "items": items,
        "product_names": product_names,
        "all_prices_found": all_prices,
        "currency": "KZT"
    }


# ---------------- Output helpers ----------------
def print_readable(data: dict) -> None:
    print("=== RECEIPT SUMMARY ===")
    print(f"Branch: {data['meta'].get('branch')}")
    print(f"BIN: {data['meta'].get('bin')}")
    print(f"Check #: {data['meta'].get('check_number')}")
    print(f"Date: {data['date_time'].get('date')}  Time: {data['date_time'].get('time')}")
    print(f"Payment: {data['payment'].get('method')}  Amount: {data['payment'].get('amount')}")
    print(f"Total (printed): {data['totals'].get('total_printed')}")
    print(f"Total (calculated): {data['totals'].get('total_calculated_from_items')}")
    print()
    print("=== ITEMS ===")
    for it in data["items"]:
        print(f"{it['index']}. {it['name']}")
        print(f"   qty={it['qty']}  unit={it['unit_price']}  total={it['line_total']}")
    print()
    print(f"All prices found count: {len(data['all_prices_found'])}")

def main():
    text = read_text("raw.txt")
    data = parse_receipt(text)

    # 1) Readable text output
    print_readable(data)

    # 2) JSON output file
    Path("parsed_receipt.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print("\nSaved: parsed_receipt.json")

if __name__ == "__main__":
    main()