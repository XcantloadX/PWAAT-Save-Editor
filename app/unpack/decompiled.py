import struct
from typing import TypeAlias, Union, Literal
from enum import IntEnum

Language: TypeAlias = Union[
    Literal['en'],
    Literal['jp'],
    Literal['hans'],
    Literal['hant'],
    Literal['fr'],
    Literal['de'],
    Literal['ko'],
]

language_suffix: dict[Language, str] = {
    'en': '_u',
    'jp': '',
    'hans': '_s',
    'hant': '_t',
    'fr': '_f',
    'de': '_g',
    'ko': '_k',
}

# Converted from decomplied code
class ConvertLineData:
    class Data:
        def __init__(self, id: int, text: list[str]):
            self.id = id
            self.text = text
            
        def __repr__(self) -> str:
            return f'<Data id={self.id} text={self.text}>'

    def __init__(self, bytes: bytes, language: str):
        self.data_: list[ConvertLineData.Data] = []
        num = 0
        while num + 2 <= len(bytes):
            item = ConvertLineData.Data(0, [])
            list2 = []
            item.id = struct.unpack_from('<H', bytes, num)[0]
            num += 2
            flag = True
            while flag and num + 2 <= len(bytes):
                stringBuilder = []
                while num + 2 <= len(bytes):
                    c = struct.unpack_from('<H', bytes, num)[0]
                    num += 2
                    if c == ord(','):
                        break
                    if c == 0:
                        flag = False
                        break
                    stringBuilder.append(chr(c))

                text = ''.join(stringBuilder)
                if language == 'JAPAN':
                    pass
                else:
                    text = self.en_to_half(text, language)
                
                text = text.replace('φ', ' ')
                list2.append(text)
            
            item.text = list2
            self.data_.append(item)

    def en_to_half(self, text: str, language: str):
        # Convert full-width alphanumeric characters to half-width
        half_width_text = ''
        for char in text:
            if '０' <= char <= '９':
                half_width_text += chr(ord(char) - ord('０') + ord('0'))
            elif 'Ａ' <= char <= 'Ｚ':
                half_width_text += chr(ord(char) - ord('Ａ') + ord('A'))
            elif 'ａ' <= char <= 'ｚ':
                half_width_text += chr(ord(char) - ord('ａ') + ord('a'))
            elif char == '　':
                half_width_text += ' '
            else:
                half_width_text += char
        return half_width_text

    def get_text(self, id: int, line: int):
        for item in self.data_:
            if item.id == id and line < len(item.text):
                return item.text[line]
        return ''

    def get_texts(self, id: int) -> list[str]:
        for item in self.data_:
            if item.id == id:
                return item.text
        return []

    @property
    def data(self):
        return self.data_


class TitleTextID(IntEnum):
    NEW_GAME = 0
    CONTINUE = 1
    OPTION = 2
    PLAY_TITLE = 3
    PLAY_EPISODE = 4
    PLAY_CONFIRM = 5
    YES = 6
    NO = 7
    TITLE_NAME = 8
    EPISODE_NUMBER = 9
    GS1_SCENARIO_NAME = 10
    GS2_SCENARIO_NAME = 11
    GS3_SCENARIO_NAME = 12
    EXIT = 13
    EXIT_MESSAGE = 14
    START_INPUT = 19
    

class SaveTextID(IntEnum):
    SELECT_SLOT = 0
    SELECT_DATA_SW = 1
    SELECT_DATA = 2
    NO_DATA_SW = 3
    NO_DATA = 4
    SELECT_CONFIRM_SW = 5
    SELECT_CONFIRM = 6
    LOADDING_SW = 7
    LOADDING = 8
    OVERWRITE_SW = 9
    OVERWRITE = 10
    SAVING_SW = 11
    SAVING_XO = 12
    SAVING_PS4 = 13
    SAVING_STEAM = 14
    CLEAR_SAVE = 15
    ADD_NEW_EPISODE = 16
    GS1_SC0 = 17
    GS1_SC1_0 = 18
    GS1_SC1_1 = 19
    GS1_SC1_2 = 20
    GS1_SC1_3 = 21
    GS1_SC2_0 = 22
    GS1_SC2_1 = 23
    GS1_SC2_2 = 24
    GS1_SC2_3 = 25
    GS1_SC2_4 = 26
    GS1_SC2_5 = 27
    GS1_SC3_0 = 28
    GS1_SC3_1 = 29
    GS1_SC3_2 = 30
    GS1_SC3_3 = 31
    GS1_SC3_4 = 32
    GS1_SC3_5 = 33
    GS1_SC4_0 = 34
    GS1_SC4_1_0 = 35
    GS1_SC4_1_1 = 36
    GS1_SC4_2 = 37
    GS1_SC4_3_0 = 38
    GS1_SC4_3_1 = 39
    GS1_SC4_4 = 40
    GS1_SC4_5_0 = 41
    GS1_SC4_5_1 = 42
    GS1_SC4_5_2 = 43
    GS2_SC0_0 = 44
    GS2_SC0_1 = 45
    GS2_SC1_0 = 46
    GS2_SC1_1_0 = 47
    GS2_SC1_1_1 = 48
    GS2_SC1_2 = 49
    GS2_SC1_3_0 = 50
    GS2_SC1_3_1 = 51
    GS2_SC2_0 = 52
    GS2_SC2_1_0 = 53
    GS2_SC2_1_1 = 54
    GS2_SC2_2 = 55
    GS2_SC2_3_0 = 56
    GS2_SC2_3_1 = 57
    GS2_SC3_0_0 = 58
    GS2_SC3_0_1 = 59
    GS2_SC3_1_0 = 60
    GS2_SC3_1_1 = 61
    GS2_SC3_2_0 = 62
    GS2_SC3_2_1 = 63
    GS2_SC3_3_0 = 64
    GS2_SC3_3_1 = 65
    GS3_SC0_0 = 66
    GS3_SC0_1 = 67
    GS3_SC1_0 = 68
    GS3_SC1_1 = 69
    GS3_SC1_2 = 70
    GS3_SC1_3_0 = 71
    GS3_SC1_3_1 = 72
    GS3_SC2_0 = 73
    GS3_SC2_1_0 = 74
    GS3_SC2_2 = 75
    GS3_SC2_3_0 = 76
    GS3_SC2_3_1 = 77
    GS3_SC3_0_0 = 78
    GS3_SC3_0_1 = 79
    GS3_SC4_0_0 = 80
    GS3_SC4_0_1 = 81
    GS3_SC4_1_0 = 82
    GS3_SC4_1_1 = 83
    GS3_SC4_2_0 = 84
    GS3_SC4_2_1 = 85
    GS3_SC4_3_0 = 86
    GS3_SC4_3_1 = 87
    GS3_SC4_3_2 = 88
    LOAD_ERROR = 90
    DELETING = 91
    SAVE_ERROR = 92
    CREATE_ERROR = 93
