from dataclasses import dataclass

@dataclass
class Sentence:
    speaker: str
    text: str

    def format(self):
        return f"{self.speaker}: {self.text}"

@dataclass
class TranscribeData:
    sentences: list # [Sentences]
    
    def script(self):
        return '\n'.join(s.format() for s in self.sentences)