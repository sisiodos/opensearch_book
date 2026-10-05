#!/usr/bin/env python3
"""独立したケースの選択・実行と、人が確認できる記録の保存。"""
import argparse
import importlib
import json
from pathlib import Path

import common

ROOT = Path(__file__).resolve().parent


def write_review(destination, results):
    lines = ['# 検証の実行記録', '',
             '各ケースのコード中の assert が期待結果です。以下は実際に送信したHTTP操作と応答です。', '']
    for result in results:
        lines += [f"## {result['id']}: {result['status']}", '',
                  f"第{result['chapter']}章 {result['section']} — {result['name']}", '']
        if result.get('error'):
            lines += ['```text', result['traceback'], '```', '']
        start, end = result['exchanges']
        for exchange in common.exchanges[start:end]:
            lines += [f"### {exchange['method']} {exchange['path']}", '']
            if exchange['body'] is not None:
                lines += ['リクエスト:', '', '```json',
                          json.dumps(exchange['body'], ensure_ascii=False, indent=2), '```', '']
            lines += [f"応答: HTTP {exchange['status']}", '', '```json',
                      json.dumps(exchange['response'], ensure_ascii=False, indent=2), '```', '']
        lines += ['判定時の補足:', '', '```json',
                  json.dumps(result.get('evidence'), ensure_ascii=False, indent=2), '```', '']
    (destination / 'review.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='ケース一覧を表示します（接続不要）')
    parser.add_argument('--case', action='append', default=[], help='実行するケースID（複数指定可）')
    parser.add_argument('--chapter', type=int, help='指定した章だけ実行します')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'cases/catalog.json').read_text())
    unknown = set(args.case) - {entry['id'] for entry in catalog}
    if unknown:
        parser.error('不明なケースID: ' + ', '.join(sorted(unknown)))
    selected = [entry for entry in catalog
                if (not args.case or entry['id'] in args.case)
                and (args.chapter is None or entry['chapter'] == args.chapter)]
    if not selected:
        parser.error('対象のケースがありません')
    if args.list:
        for entry in selected:
            print(f"{entry['id']}  {entry['section']}  {entry['name']}")
        return

    # 過去の実機記録を保持し、今回の結果は実行ごとのディレクトリへ保存します。
    destination = ROOT / 'runs' / common.PREFIX.rstrip('-')
    destination.mkdir(parents=True)
    run_prefix = common.PREFIX
    try:
        info = common.req('GET', '/')
        (destination / 'environment.json').write_text(json.dumps(info, ensure_ascii=False, indent=2))
        print(f"OpenSearch {info['version']['number']} / Lucene {info['version']['lucene_version']}")
        for entry in selected:
            common.PREFIX = run_prefix + entry['id'] + '-'
            module = importlib.import_module('cases.' + entry['id'])
            common.case(entry['chapter'], entry['section'], entry['name'], module.run)
            common.results[-1]['id'] = entry['id']
    finally:
        (destination / 'results.json').write_text(json.dumps(
            {'prefix': run_prefix, 'results': common.results, 'indexes': common.indexes},
            ensure_ascii=False, indent=2))
        (destination / 'exchanges.json').write_text(json.dumps(common.exchanges, ensure_ascii=False, indent=2))
        write_review(destination, common.results)
        print(f'記録: {destination.relative_to(ROOT.parent)}/review.md')
    passed = sum(result['status'] == 'PASS' for result in common.results)
    failed = sum(result['status'] == 'FAIL' for result in common.results)
    print(f'PASS={passed} FAIL={failed}')
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
