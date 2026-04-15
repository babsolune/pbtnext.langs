#!/usr/bin/env python3
"""
langs.json generator
"""

import json
import os
import sys
import configparser


def parse_ini(filepath: str) -> dict:
    parser = configparser.RawConfigParser()
    parser.optionxform = str  # conserver la casse des clés
    try:
        with open(filepath, encoding="utf-8") as f:
            content = "[root]\n" + f.read()
        parser.read_string(content)
        return {k: v.strip('"') for k, v in dict(parser["root"]).items()}
    except Exception:
        return {}


def generate_langs_json(addons_dir: str) -> list:
    entries = []

    for addon_id in os.listdir(addons_dir):
        addon_path = os.path.join(addons_dir, addon_id)
        if not os.path.isdir(addon_path):
            continue

        config_file = os.path.join(addon_path, "config.ini")
        if not os.path.isfile(config_file):
            continue

        config = parse_ini(config_file)
        if not config or config.get("addon_type") != "lang":
            continue

        entries.append({
            "id":            addon_id,
            "addon_type":    config.get("addon_type",    "lang"),
            "compatibility": config.get("compatibility", ""),
            "version":       config.get("version",       ""),
            "author":        config.get("author",        ""),
            "author_mail":   config.get("author_mail",   ""),
            "author_link":   config.get("author_link",   ""),
            "creation_date": config.get("creation_date", ""),
            "last_update":   config.get("last_update",   ""),
            "identifier":    config.get("identifier",    ""),
            "name":          config.get("name",          addon_id),
        })

    entries.sort(key=lambda e: e["id"].lower())
    return entries


def main():
    addons_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isdir(addons_dir):
        print(f"Dossier '{addons_dir}' introuvable.", file=sys.stderr)
        sys.exit(1)

    entries     = generate_langs_json(addons_dir)
    output_file = os.path.join(addons_dir, "langs.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

    print(f"Généré : {output_file}")
    print(f"{len(entries)} addon(s) indexé(s).")


if __name__ == "__main__":
    main()
