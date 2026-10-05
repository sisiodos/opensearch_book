"""第8章 8.3: book distance, box and polygon queries on points

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import expect_ids, fragments, geo_fixture, ids

def run():
    i = geo_fixture('geoqueries')
    out = []
    for b in fragments(8):
        q = b.get('query', {})
        kind = next(iter(q), '')
        if kind not in ('geo_distance', 'geo_bounding_box', 'geo_shape'):
            continue
        wanted = ['west'] if kind == 'geo_shape' else ['station']
        r = expect_ids(i, q, wanted)
        out.append({
            'query_type': kind,
            'ids': sorted(ids(r)),
        })
    return out
