import MeCab
import dill
from train.concept.crf_util import sent2features
import re


# 発話文から対話行為タイプとコンセプトを抽出するクラス
class DA_Concept:

    def __init__(self):
        # MeCabの初期化
        self.mecab = MeCab.Tagger()
        self.mecab.parse('')

        # SVMモデルの読み込み
        with open("train/dialogue_act/svc.model", "rb") as f:
            self.vectorizer = dill.load(f)
            self.label_encoder = dill.load(f)
            self.svc = dill.load(f)

        # CRFモデルの読み込み
        with open("train/concept/crf.model", "rb") as f:
            self.crf = dill.load(f)

    # 発話文から対話行為タイプとコンセプトを抽出
    def process(self, utt):
        lis = []
        for line in self.mecab.parse(utt).splitlines():
            if line == "EOS":
                break
            else:
                word, feature_str = line.split("\t")
                features = feature_str.split(',')
                postag = features[0]
                lis.append([word, postag, "O"])

        words = [x[0] for x in lis]
        tokens_str = " ".join(words)
        X = self.vectorizer.transform([tokens_str])
#         print(X)
        Y = self.svc.predict(X)
#         print(Y)
        # 数値を対応するラベルに戻す
        da = self.label_encoder.inverse_transform(Y)[0]

        X = [sent2features(s) for s in [lis]]

        # 各単語に対応するラベル列
        labels = self.crf.predict(X)[0]

        # 単語列とラベル系列の対応を取って辞書に変換
        conceptdic = {}
        buf = ""
        last_label = ""
        for word, label in zip(words, labels):
            if re.search(r'^B-', label):
                if buf != "":
                    _label = last_label.replace('B-', '').replace('I-', '')
                    conceptdic[_label] = buf
                buf = word
            elif re.search(r'^I-', label):
                buf += word
            elif label == "O":
                if buf != "":
                    _label = last_label.replace('B-', '').replace('I-', '')
                    conceptdic[_label] = buf
                    buf = ""
            last_label = label
        if buf != "":
            _label = last_label.replace('B-', '').replace('I-', '')
            conceptdic[_label] = buf

        return da, conceptdic


if __name__ == '__main__':
    da_concept = DA_Concept()
    da, conceptdic = da_concept.process("ちくわについて教えて")
    print(da, conceptdic)
