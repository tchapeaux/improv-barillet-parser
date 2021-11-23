# coding: utf-8

import csv
import sys
from collections import namedtuple
import xml.etree.ElementTree as ET
import codecs

Impro = namedtuple("Impro", ["nature", "titre", "nbj", "cate", "duree", "divers"])


def get_impro_element(impro):
    impro_xml = ET.Element("impro")
    nature_xml = ET.SubElement(impro_xml, "nature")
    nature_xml.text = impro.nature
    titre_xml = ET.SubElement(impro_xml, "titre")
    titre_xml.text = impro.titre
    nbj_xml = ET.SubElement(impro_xml, "nbj")
    nbj_xml.text = impro.nbj
    cate_xml = ET.SubElement(impro_xml, "cate")
    cate_xml.text = impro.cate
    cate_xml.set('isLibre', "1" if impro.cate == 'L' else "0")
    duree_xml = ET.SubElement(impro_xml, "duree")
    duree_xml.text = impro.duree
    divers_xml = ET.SubElement(impro_xml, "divers")
    divers_xml.text = impro.divers
    return impro_xml


impros = []
with codecs.open(sys.argv[1], "r", "utf-8") as f:
    for line in [l.strip() for l in f.readlines() if len(l.strip()) > 0]:
        line = line.split(",")
        impros.append(
            Impro(
                nature=line[0].strip('"'),
                titre=line[1].strip('"'),
                nbj=line[2].strip('"'),
                cate=line[3].strip('"'),
                duree=line[4].strip('"'),
                divers=" ".join(line[5:]),
            )
        )

with open("impro_out.xml", "w") as f:
    barillet_xml = ET.Element("barillet")
    for impro in impros:
        print("Parsed Impro: ", impro)
        barillet_xml.append(get_impro_element(impro))
    barillet_xml_str = str(
        ET.tostring(
            barillet_xml, encoding="unicode", method="xml", xml_declaration=True
        )
    )
    # Quick&dirty: add css stylesheet to xm
    barillet_xml_str = barillet_xml_str.replace(
        "<?xml version='1.0' encoding='UTF-8'?>",
        """<?xml version='1.0' encoding='UTF-8'?>\n<?xml-stylesheet href="impro_barillet.css"?>""",
    )
    f.write(barillet_xml_str)
    f.write("\n")
