# /whatsnews/lib/deepl.py

import deepl


deepl_client = None


def deepl_init(api_key):
    global deepl_client
    deepl_client = deepl.DeepLClient(api_key)


def translate_strs(strs):
    results = deepl_client.translate_text(strs, target_lang='EN-US')
    strs1 = [res.text for res in results]
    return strs1