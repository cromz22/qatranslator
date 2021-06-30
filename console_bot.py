from asr_google_streaming_vad import MicrophoneStream, GoogleStreamingASR
from tts_google import GoogleTextToSpeech


class ConsoleBot:
    def __init__(self, system):
        self.system = system

    def start(self, input_utt):
        # 辞書型 inputにユーザIDを設定
        input = {'utt': None, 'sessionId': "myid"}

        # システムからの最初の発話をinitial_messageから取得し，送信
        return self.system.initial_message(input)

    def message(self, input_utt):
        # 辞書型 inputにユーザからの発話とユーザIDを設定
        input = {'utt': input_utt, 'sessionId': "myid"}

        # replyメソッドによりinputから発話を生成
        system_output = self.system.reply(input)

        # 発話を送信
        return system_output

    def run(self):
        sys_out = self.start("")
        tts = GoogleTextToSpeech()
        while True:
            print("YOU:")
            mic_stream = MicrophoneStream(16000, 1600)
            asr_stream = GoogleStreamingASR(16000, mic_stream)
            response = asr_stream.get_asr_result()
            input_utt = response.alternatives[0].transcript
            sys_out = self.message(input_utt)
            print("\nSYS: " + sys_out["utt"])
            tts.generate(sys_out["utt"])
            tts.play()

            if sys_out["end"]:
                break
