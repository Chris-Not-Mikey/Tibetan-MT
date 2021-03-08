# convert.py
# ##############################################################
# Changes .tmx format into parallel source and target txt files
# Run this with current directory structure to regenetate files
# Maintainer: Chris Calloway
# email: cmc2374@colubmia.edu
# ##############################################################

import xml.etree.ElementTree as ET
import os
tmx_tag = "{http://www.lisa.org/tmx14}"
lang_tag = "{http://www.w3.org/XML/1998/namespace}lang"


orginal_84000_dir = "./Original/84000"
for filename in os.listdir(orginal_84000_dir):

    if filename.endswith(".tmx"):
        print(filename)
        name = filename.rsplit(".", 1)[0]

        src_name = "Altered/84000/src_" + name + ".txt"
        tgt_filename = "Altered/84000/tgt_" + name + ".txt"

        src = open(src_name, "w")
        tgt = open(tgt_filename, "w")

        full_file_name = "./Original/84000/" + filename
        root = ET.parse(
            full_file_name).getroot()

        # Filter through to find body of text
        findBody = False
        body_tag = tmx_tag + "body"
        while findBody == False:
            children = root.getchildren()

            for i in children:
                if i.tag == body_tag:
                    findBody = True
                    root = i

            # Now that we have the body we look through each sentence of the source text

            # Parallel lines holds all the lines of important texts in both languages
            # One "parallel" line corresponds to a line of Tibetan text and its corresponding translation
            parallel_lines = root.getchildren()

            tuv_tag = tmx_tag + "tuv"
            counter = 0
            for i in parallel_lines:

                # Now we look in the parallel lines for each language
                sentences = i.getchildren()
                counter = counter + 1
                for j in sentences:
                    if j.tag == tuv_tag:
                        # Get Tibetan language and write to file
                        if j.get(lang_tag) == "bo":
                            sentence = j.getchildren()
                            if sentence[0].text == None:
                                src.write("")
                                continue
                            src.write(sentence[0].text)
                            src.write("\n")

                        # Get English langauge and write to file
                        if j.get(lang_tag) == "en":
                            sentence = j.getchildren()
                            if sentence[0].text == None:
                                tgt.write("")
                                continue
                            tgt.write(sentence[0].text)
                            tgt.write("\n")

            # close file objects
            src.close()
            tgt.close()
