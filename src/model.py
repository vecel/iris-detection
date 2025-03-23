from dataclasses import dataclass

@dataclass
class Model:
    image: any = None
    iris: any = None
    processing: bool = False