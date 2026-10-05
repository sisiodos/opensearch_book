"""第3章 3.2–3.3: field capabilities by type

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import basic_fixture, req

def run():
    basic = basic_fixture()
    return req('GET', f'/{basic}/_field_caps?fields=*')
