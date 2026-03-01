from typing import Optional, List

import requests

def save_file():
    pass

def get_fact(url: str, headers: dict, facts_count: int = 10) -> Optional[List[str]]:
    facts = []
    for i in range(facts_count):
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        if not response:
            continue
        data = response.json()
        if not data.get("fact"):
            return None
        fact = data.get('fact')
        if fact in facts:
            i -= 1
            continue
        facts.append(fact)
    return facts

def save_facts(file_name: str, facts: List[str]) -> None:
    if facts:
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                for i,fact in enumerate(facts):
                    f.write(f"Факт №{i + 1}: {fact} \n")
            print(f"Файл facts.txt успешно сохранен")
        except Exception as e:
            print(f"Error: {e}")




if __name__ == "__main__":
    base_url = "https://catfact.ninja/fact"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    file_name = "facts.txt"

    facts = get_fact(base_url, headers)
    if not facts:
        print("No fact found")
    save_facts(file_name, facts)