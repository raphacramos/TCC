import re

text_final = "1 5 MARTENS Lukas GER 0.70 3:42.35"
text_heat = "1 4 4 SHORT Samuel AUS 17 SEP 2003 0.65 3:42.07 Q"
text_heat_dsq = "12 3 5 NOME Alguem BRA 12 JUN 2002 DSQ"

padrao_atleta = re.compile(r'^(\d+)\s+(?:(\d+)\s+)?(\d+)\s+([A-Za-z\s\-\']+?)\s+([A-Z]{3})\s+(?:\d{1,2}\s+[A-Z]{3}\s+\d{4}\s+)?([\d.]+)?\s*([\d:.]+|DSQ|DNS)')

for t in [text_final, text_heat, text_heat_dsq]:
    print(t)
    m = padrao_atleta.match(t)
    if m:
        print(m.groups())
    else:
        print("NO MATCH")

text_split_final = "50m (1) 24.77 100m (=3) 51.95"
text_split_heat = "50m 25.39 100m 52.98"

padrao_parciais = re.compile(r'(\d+)m\s+(?:\([^)]+\)\s+)?([\d:.]+)')

print(padrao_parciais.findall(text_split_final))
print(padrao_parciais.findall(text_split_heat))
