"""第7章 7.2: kuromoji tokenizer on Japanese example

検証データを作成し、assert で期待結果を確認します。
HTTP操作は実行後の review.md と exchanges.json で確認できます。
"""
from common import analyze, tokens

def run():
    r = analyze({
        'tokenizer': 'kuromoji_tokenizer',
        'text': '私は学生です',
    })
    assert tokens(r) == ['私', 'は', '学生', 'です']
    return r['tokens']
