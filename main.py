import glob
import os
import re


def get_ts_files():
    # Klasör yolu
    klasor_yolu = 'C:/Users/emrah/Documents/GitHub/ReosMobileApp-Ionic-RealNet/src/models/enums'  # Klasör yolunu değiştirin

    # Klasördeki .dart uzantılı dosyaları alın
    dosya_listesi = glob.glob(os.path.join(klasor_yolu, '*.ts'))

    for dosya_yolu in dosya_listesi:
        with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
            dosya_icerik = dosya.read()
            create_dart_file(convert_to_dart_filename(os.path.basename(dosya_yolu)), convert_dart_enum(dosya_icerik))

def create_dart_file(file_name, file_content):
    with open(file_name, 'w', encoding='utf-8') as dart_file:
        dart_file.write(file_content)

def dart_field_snack_case (field):
    return field[0].lower() + field[1:]

def convert_to_dart_filename(file_name):
    # Dosya adındaki "enum" kelimesi varsa kaldır. Büyük küçük harf duyarlılığı olsun
    if "Enum" in file_name:
        file_name = file_name.replace("Enum", "")

    # Dosya adındaki ".ts" uzantısını kaldır
    if file_name.endswith(".ts"):
        file_name = file_name[:-3]
    
    # Camel case'i snake case'e çevir
    words = []
    word = ""
    for char in file_name:
        if char.isupper():
            if word:
                words.append(word.lower())
            word = char
        else:
            word += char
    if word:
        words.append(word.lower())

    # Kelimeleri alt çizgi ile birleştir
    dart_file_name = "_".join(words)

    return dart_file_name + ".dart"


# Metindeki enum içeriğini yakalamak için regex deseni
def convert_dart_enum(enumString):
    new_enum_string = "import 'package:json_annotation/json_annotation.dart';\n\nenum "

    pattern = r'enum\s+(\w+)\s*[\r\n]*\s*{([\s+\S+]*?)}'

    matches = re.search(pattern, enumString)

    if matches:
        enum_name = matches.group(1)
        enum_content = matches.group(2)

        enum_name = enum_name.replace("Enum", "")

        # Süslü parantez içindeki değerleri ayırmak için yeni bir regex deseni
        enum_values = re.findall(r'(\w+)\s*=\s*(\d+)', enum_content)

        new_enum_string += enum_name + " {\n"

        for value in enum_values:
            if(value != enum_values[-1]):
                new_enum_string += f"  @JsonValue({value[1]})\n  {dart_field_snack_case(value[0])}({value[1]}),\n\n"
            else:
                new_enum_string += f"  @JsonValue({value[1]})\n  {dart_field_snack_case(value[0])}({value[1]});\n\n"
        
        new_enum_string += f"  const {enum_name}(this.value);\n  final int value;\n"
        new_enum_string += "}"

        return new_enum_string
    
    return "Error: No enum found in the file"

get_ts_files()

#print(convertDartEnum(input_string2))