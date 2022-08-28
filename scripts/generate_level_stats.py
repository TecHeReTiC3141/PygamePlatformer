import json
from pathlib import Path
from re import match
from pprint import pprint


def generate_blank_stats() -> dict[str, dict]:
    levels_dir = Path('levels')
    level_names = {fil.stem for fil in levels_dir.glob('*.tmx') if match(r'level\d+', fil.stem)}
    print(level_names)
    level_info = {level_name: {'locked': True, 'passed': False, 'best_time': float('inf'), 'best_score': -1, 'stars': 0}
                  for level_name in level_names}
    level_info['level1']['locked'] = False
    with open('level_stats.json', 'w', encoding='utf-8') as f:
        json.dump(level_info, f)
    with open('level_stats.json', encoding='utf-8') as f:
        return json.load(f)


def get_level_stats() -> dict[str, dict]:
    try:
        level_stats = Path('level_stats.json')
        if level_stats.exists():
            with open('level_stats.json', encoding='utf-8') as f:
                level_stats = json.load(f)
            return level_stats
        else:
            return generate_blank_stats()
    except Exception as e:
        print(e)
        return generate_blank_stats()


if __name__ == '__main__':
    generate_blank_stats()
    with open('../level_stats.json', encoding='utf-8') as f:
        level_stats = json.load(f)
    print(level_stats)
