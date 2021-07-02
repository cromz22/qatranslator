from da_concept_extractor import DA_Concept
import requests
from console_bot import ConsoleBot
import re


class QATranslator:

    nouns = ['ちくわ', '三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
             '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

    # システムの対話行為とシステム発話を紐づけた辞書
    uttdic = {"open-prompt": "ご用件をどうぞ",
              "ask-noun": "知りたいことは何ですか"}

    def __init__(self):
        # 対話セッションを管理するための辞書
        self.sessiondic = {}
        # 対話行為タイプとコンセプトを抽出するためのモジュールの読み込み
        self.da_concept = DA_Concept()

    def get_abstract_from_wikipedia(self, noun: str) -> str:
        url = f"https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={noun}"

        response = requests.get(url)
        res_json = response.json()

        abstract = []
        for id in res_json["query"]["pages"]:
            if id == "-1":
                print(f"Sorry, I don't know the word {noun}")
                return ""
            else:
                abstract = [res_json["query"]["pages"][id]["extract"]
                            for id in res_json["query"]["pages"]]

        return abstract[0].split("\n")[0]

    def get_translation_from_google(self, target: str, text: str) -> str:
        """Translates text into the target language.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """
        import six
        from google.cloud import translate_v2 as translate

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, target_language=target)

        return result["translatedText"]

    # 発話から得られた情報をもとにフレームを更新
    def update_frame(self, frame, da, conceptdic):
        if da == "ask-question":
            for k, v in conceptdic.items():
                # コンセプトの情報でスロットを埋める
                frame[k] = v
        elif da == "initialize" or da == "greetings":
            frame = {"noun": ""}
        elif da == "correct-info":
            for k, v in conceptdic.items():
                if frame[k] == v:
                    frame[k] = ""
        return frame

    # フレームの状態から次のシステム対話行為を決定
    def next_system_da(self, frame):
        # すべてのスロットが空であればオープンな質問を行う
        if frame["noun"] == "":
            return "open-prompt"
        # 空のスロットがあればその要素を質問する
        elif frame["noun"] == "":
            return "ask-noun"
        else:
            return "tell-info"

    def initial_message(self, input):
        sessionId = input["sessionId"]

        # セッションIDとセッションに関連する情報を格納した辞書
        self.sessiondic[sessionId] = {
            "frame": {"noun": ""}}

        return {"utt": "こちらは翻訳機能付き質問応答システムです。ご用件をどうぞ。", "end": False}

    def reply(self, input):
        text = input["utt"]
        sessionId = input["sessionId"]

        # 現在のセッションのフレームを取得
        frame = self.sessiondic[sessionId]["frame"]
        # print("frame=", frame)

        # 発話から対話行為タイプとコンセプトを取得
        da, conceptdic = self.da_concept.process(text)
        # print(da, conceptdic)

        # 対話行為タイプとコンセプトを用いてフレームを更新
        frame = self.update_frame(frame, da, conceptdic)
        # print("updated frame=", frame)

        # 更新後のフレームを保存
        self.sessiondic[sessionId] = {"frame": frame}

        # フレームからシステム対話行為を得る
        sys_da = self.next_system_da(frame)

        # 遷移先がtell-infoの場合は情報を伝えて終了
        if sys_da == "tell-info":
            noun = frame["noun"]
            print(f"recognized noun: {noun}")

            abstract = self.get_abstract_from_wikipedia(noun)
            cleaned_abstract = re.sub(r"（[^）]*）", "", abstract)
            print(f"Japanese abstract: {cleaned_abstract}")
            translated_abstract = self.get_translation_from_google("en", cleaned_abstract)

            del self.sessiondic[sessionId]
            return {"utt": translated_abstract, "end": True}

        else:
            # その他の遷移先の場合は状態に紐づいたシステム発話を生成
            sysutt = self.uttdic[sys_da]
            return {"utt": sysutt, "end": False}


if __name__ == '__main__':
    system = QATranslator()
    bot = ConsoleBot(system)
    bot.run()
