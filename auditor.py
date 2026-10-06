"""Password strength auditor — SYA203 egitim araci (stdlib only).
Kullanim: python auditor.py "OrnekSifre123!"
"""
import argparse
import math
import string

COMMON = {
    "123456", "password", "123456789", "qwerty", "12345678",
    "admin", "letmein", "welcome", "123123", "abc123",
}


def charset_size(parola: str) -> int:
    size = 0
    if any(c.islower() for c in parola):
        size += 26
    if any(c.isupper() for c in parola):
        size += 26
    if any(c.isdigit() for c in parola):
        size += 10
    if any(c in string.punctuation for c in parola):
        size += len(string.punctuation)
    return size or 1


def entropy_bits(parola: str) -> float:
    return len(parola) * math.log2(charset_size(parola))


def crack_time(bits: float, guesses_per_sec: float = 1e10) -> str:
    seconds = (2 ** bits) / guesses_per_sec
    if seconds < 60:
        return f"{seconds:.1f} saniye"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f} dakika"
    hours = minutes / 60
    if hours < 48:
        return f"{hours:.1f} saat"
    years = seconds / 31_556_952
    if years < 1:
        return f"{seconds / 86400:.1f} gun"
    if years > 1e6:
        return "1 milyon yildan fazla"
    return f"{years:,.0f} yil"


def audit(parola: str) -> dict:
    bits = entropy_bits(parola)
    if parola.lower() in COMMON:
        seviye = "COK ZAYIF (yaygin parola)"
    elif bits < 40:
        seviye = "ZAYIF"
    elif bits < 60:
        seviye = "ORTA"
    elif bits < 80:
        seviye = "GUCLU"
    else:
        seviye = "COK GUCLU"
    return {"uzunluk": len(parola), "entropi": round(bits, 1),
            "seviye": seviye, "kirilmasure": crack_time(bits)}


def main() -> None:
    ap = argparse.ArgumentParser(description="Parola gucluluk denetimi (egitim amacli)")
    ap.add_argument("parola", help="Denetlenecek parola")
    args = ap.parse_args()
    for k, v in audit(args.parola).items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
