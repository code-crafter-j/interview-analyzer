import assemblyai as aai
from Models import Sentence, TranscribeData
from typing import List, Dict

class Transcribe():

    def __init__(self):
        aai.settings.api_key = "assembly api key"

    def transcribe_AAI(self, audioFilePath, language_code):
        """
        Transcribes an audio file using AssemblyAI's SDK
        """
        config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best,
                                         language_code=language_code, 
                                         speaker_labels=True, 
                                         speakers_expected=2)
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audioFilePath)
        
        sentences = []
        for u in transcript.utterances:
            speaker = f"Speaker {u.speaker}"
            sentences.append(Sentence(speaker=speaker, text=u.text))

        return TranscribeData(sentences=sentences)
    
    def format_transcription(self, data: TranscribeData):
        formatted_string = ""
        for sentence in data.sentences:
            formatted_string += f"{sentence.speaker}: {sentence.text}\n"
        return formatted_string.strip()
    
    def convert_format(self, transcribe_data: TranscribeData) -> Dict[str, List[str]]:
        result = {}
        for sentence in transcribe_data.sentences:
            speaker_key = sentence.speaker
            if speaker_key not in result:
                result[speaker_key] = []
            result[speaker_key].append(sentence.text)
        return result
    
    def parse_string_to_transcribedata(self, input_str: str) -> TranscribeData:
        sentences = []
        for line in input_str.split('\n'):
            if line.strip():  # Check if the line is not empty
                speaker, text = line.split(': ', 1)
                sentences.append(Sentence(speaker=speaker.strip(), text=text.strip()))
        return TranscribeData(sentences=sentences)