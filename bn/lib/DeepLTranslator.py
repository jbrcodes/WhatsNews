# /bn/lib/DeepLTranslator.py

import deepl


LangsBeta = ('fa', 'hi')  # Persian, Hindi


deepl_client = None


class DeepLTranslator():

    @classmethod
    def init(cls, api_key):
        global deepl_client
        deepl_client = deepl.DeepLClient(api_key)


    def translate_strings(self, strs_src, lang_src, lang_dest):
        lang_dest1 = 'en-us' if lang_dest == 'en' else lang_dest
        if lang_src in LangsBeta or lang_dest1 in LangsBeta:
            results = deepl_client.translate_text(strs_src, source_lang=lang_src, target_lang=lang_dest1, \
                extra_body_parameters={ 'enable_beta_languages': True })
        else:
            results = deepl_client.translate_text(strs_src, source_lang=lang_src, target_lang=lang_dest1)
        strs_dest = [r.text for r in results]
        return strs_dest