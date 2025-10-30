#!/usr/bin/env python3
import time
from datetime import datetime, timedelta, timezone

LOCAL_TZ = datetime.now().astimezone().tzinfo  # your local TZ

def epoch_seconds(dt_utc: datetime) -> int:
    """Return Unix time in whole seconds from a UTC datetime."""
    return int(dt_utc.timestamp())

def to_iso(dt: datetime) -> str:
    """ISO 8601 with timezone offset."""
    return dt.isoformat(timespec="seconds")

def show_dt_from_epoch(ts_raw: str):
    """Accept seconds (10d) or milliseconds (13d); print UTC and local."""
    ts_raw = ts_raw.strip()
    try:
        n = int(ts_raw)
    except ValueError:
        print("✗ Not a number.")
        return

    # Heuristic: >= 1e11 → milliseconds
    if abs(n) >= 100_000_000_000:
        seconds = n / 1000.0
    else:
        seconds = n

    dt_utc = datetime.fromtimestamp(seconds, tz=timezone.utc)
    dt_local = dt_utc.astimezone(LOCAL_TZ)

    print(f"\nParsed as {'milliseconds' if abs(n) >= 1e11 else 'seconds'} since epoch:")
    print(f"  UTC   : {to_iso(dt_utc)}")
    print(f"  Local : {to_iso(dt_local)}\n")

def make_offsets_menu(now_utc: datetime):
    options = [
        ("now", timedelta(minutes=0)),
        ("-2 minutes", timedelta(minutes=2)),
        ("-5 minutes", timedelta(minutes=5)),
        ("-10 minutes", timedelta(minutes=10)),
        ("-15 minutes", timedelta(minutes=15)),
        ("-30 minutes", timedelta(minutes=30)),
        ("-45 minutes", timedelta(minutes=45)),
        ("-1 hour 30 minutes", timedelta(hours=1, minutes=30)),
    ]
    print("\nChoose offset:")
    for i, (label, _) in enumerate(options, 1):
        print(f"  {i}) {label}")
    choice = input("Enter 1-8: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
        print("✗ Invalid choice.")
        return
    label, delta = options[int(choice) - 1]
    target_utc = now_utc - delta
    ts = epoch_seconds(target_utc)
    print(f"\n{label}:")
    print(f"  Unix seconds (10 digits): {ts}")
    print(f"  UTC   : {to_iso(target_utc)}")
    print(f"  Local : {to_iso(target_utc.astimezone(LOCAL_TZ))}\n")

def show_now_timestamp():
    now_utc = datetime.now(timezone.utc)
    ts = epoch_seconds(now_utc)
    print("\nCurrent time:")
    print(f"  Unix seconds (10 digits): {ts}")
    print(f"  UTC   : {to_iso(now_utc)}")
    print(f"  Local : {to_iso(now_utc.astimezone(LOCAL_TZ))}\n")

def main():
    while True:
        print("What do you want to do?")
        print("  1) Transform timestamp → date")
        print("  2) Produce new timestamp(s) from current time")
        print("  3) Show current timestamp (quick)")
        print("  0) Exit")
        choice = input("Enter 0-3: ").strip()

        if choice == "1":
            ts_raw = input("Enter Unix timestamp (seconds or milliseconds): ")
            show_dt_from_epoch(ts_raw)
        elif choice == "2":
            now_utc = datetime.now(timezone.utc)
            make_offsets_menu(now_utc)
        elif choice == "3":
            show_now_timestamp()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("✗ Invalid choice.\n")

if __name__ == "__main__":
    main()
