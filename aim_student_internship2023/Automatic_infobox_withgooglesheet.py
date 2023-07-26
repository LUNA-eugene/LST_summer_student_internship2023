# pip install pythainlp

# วัด
syn_วัด = {'location': ['ที่ตั้ง', 'ตั้งอยู่', 'ที่อยู่'],
 'type': ['ประเภท', 'เป็น'],
 'sect': ['นิกาย', 'ฝ่าย', 'สังกัด', 'ในสังกัด']}

# วัง
syn_วัง = {'type': ['ประเภท', 'เป็น'],
 'location': ['ที่ตั้ง' ,'ที่อยู่',  'ตั้งอยู่' ],
 'status': ['สถานะ'],
 'city': ['เมือง', 'จังหวัด'],
 'country': ['ประเทศ'],
 'start building': ['เริ่มสร้าง', 'ก่อตั้ง', 'สร้าง' ,'สร้างเมื่อ', 'สร้างขึ้นเมื่อ']}

# อุทยานแห่งชาติ
syn_อุทยานแห่งชาติ = {'location': ['ที่ตั้ง','ที่อยู่' , 'ตั้งอยู่', 'ตั้งอยู่ที่' , 'ตั้งอยู่ใน'],
 'area': ['พื้นที่', 'ขนาด', 'เนื้อที่'],
 'government agency': ['หน่วยราชการ', 'กรม'],
 'establish': ['จัดตั้ง', 'จัดตั้งเป็นอุทยานแห่งชาติเมื่อ'],
 'coordinates': ['พิกัด', 'พิกัดทางภูมิศาสตร์']}

# สถาบันอุดมศึกษา
syn_สถาบันอุดมศึกษา = {'type': ['ประเภท', 'เป็น'],
 'website': ['เว็บไซต์', 'website', 'เว็บ'],
 'location': ['ที่ตั้ง', 'ที่อยู่' ,  'ตั้งอยู่'],
 'initials': ['ชื่อย่อ', 'อักษรย่อ'],
 'establish': ['สถาปนา', 'เมื่อ', 'ก่อตั้งขึ้นเมื่อ', 'ก่อตั้งขึ้นเมื่อวันที่']}

# โรงพยาบาล
syn_โรงพยาบาล = {'location': ['ที่ตั้ง', 'ที่อยู่' ,  'ตั้งอยู่'],
 'type': ['ประเภท', 'เป็น'],
 'number of beds': ['จำนวนเตียง', 'ขนาด', 'จำนวน'],
 'website': ['เว็บไซต์'],
 'affiliation': ['สังกัด']}

# default
syn_default = {'location': ['ที่ตั้ง', 'ที่อยู่' ,  'ตั้งอยู่'],
               'name': ['ชื่อ', 'เป็น'],
               'type': ['ประเภท', 'เป็น'],
               'Related person': ['บุคคลที่เกี่ยวข้อง']}

def template_infobox_place(data, name_rule_temple = 'isTemple01' , name_rule_palace = 'isPalace01', name_rule_nationalpark = 'isNationalPark01', 
                           name_rule_university = 'isUniversity01', name_rule_hospital = 'isHospital01', name_rule_default = 'isDefault01'):
                           
    from pythainlp.util import normalize
    import re
    import pandas as pd
    import ast


    def postag_ner(data):
        from pythainlp.tag import pos_tag
        from pythainlp.tokenize import word_tokenize
        from pythainlp.tag import NER

        ner = NER("thainer")
        data_ner = ner.tag(data)

        data_ner_modified = [list(tup) for tup in data_ner]
        words = []
        for word in data_ner_modified:
            words.append(word[0])

        data_pos_modified = [list(tup) for tup in pos_tag(words)]

        merged_list = [data_ner_modified[i] + data_pos_modified[i] for i in range(len(data_ner_modified))]
        data_ner_pos =  [sublist[:2] + sublist[3:] for sublist in merged_list]
        data_ner_pos = [item for item in data_ner_pos if item != [' ', 'O', 'PUNC']]
        return(data_ner_pos)

    def extract_location(data_ner_pos, syn_words = ['ที่ตั้ง', 'ตั้งอยู่', 'ที่อยู่'] , wordNERsearch = 'L', wordNER_B = 'B-LOCATION', wordNER_I = 'I_LOCATION', 
                     wordNERsearch_1_2 = '-ZIP', wordis = 'จังหวัด', wordNERis = 'O', wordis_1_2 = 'เลขที่', nextwordPOS = 'DCNM',
                     wordPOSis = 'DCNM',wordPOSis_2 = 'VACT', nextwordPOS_2 = 'NCMN'):
    
        value_location = ''
        for i in range(len(data_ner_pos)):
            if data_ner_pos['Word'][i] in syn_words:
                for x in range(i + 1, i + 5):
                    if re.search(wordNERsearch , data_ner_pos['NER'][x]):
                        for j in range(i + 1, i + 15):
                            #if data_ner_pos['POS tags'][j] in ['RPRE', 'JCRG']:
                                #value_location += data_ner_pos['Word'][j]
                            if data_ner_pos['NER'][j] == wordNER_B:
                                value_location += ' ' + data_ner_pos['Word'][j] 
                            elif data_ner_pos['NER'][j] == wordNER_I:
                                value_location += data_ner_pos['Word'][j] 
                            elif re.search(wordNERsearch_1_2, data_ner_pos['NER'][j]):
                                value_location += data_ner_pos['Word'][j] + ' '

                            # จังหวัด
                            elif data_ner_pos['Word'][j] == wordis and data_ner_pos['NER'][j] == wordNERis:
                                value_location += ' ' + data_ner_pos['Word'][j] 
                                value_location += data_ner_pos['Word'][j+1] 
                            # เลขที่
                            elif data_ner_pos['Word'][j] == wordis_1_2:
                                value_location += data_ner_pos['Word'][j] + ' '
                                if data_ner_pos['POS tags'][j+1] == nextwordPOS:
                                    value_location += data_ner_pos['Word'][j+1] + ' ' 
                            # รหัสไปรษณีย์
                            elif data_ner_pos['POS tags'][j] == wordPOSis and len(data_ner_pos['Word'][j])== 5:
                                value_location += data_ner_pos['Word'][j]
                        value_location += ','  
                        break
        
                    elif data_ner_pos['POS tags'][x] == wordPOSis_2 and data_ner_pos['POS tags'][x+1] == nextwordPOS_2 :
                        value_location += data_ner_pos['Word'][x]
                        value_location += data_ner_pos['Word'][x+1]
                #break
                        
        return value_location

    def find_value_nextword(df, word, syn_words = ['ประเภท', 'เป็น'] ):
        value = ''
        import re
        for i in range(len(df)):
            if df['Word'][i] in syn_words:
                value += df['Word'][i]
                for j in range(i + 1, i + 3):
                    value += df['Word'][j] + ' '
                    if re.search(word, df['Word'][j+1]):
                        value += df['Word'][j+1]
                    break
        return value

    def find_value_nextword_search(df, syn_words, wordNER):
        value = ''
        import re
        for i in range(len(df)):
            if df['Word'][i] in syn_words:
                for j in range(i+1, i+17):
                    if re.search(wordNER, df['NER'][j]):
                        value += df['Word'][j]
                break
                    
        return value      


    def find_date(df, syn_words, wordsPOS, nextwordsPOS, wordsNER):
        import re
        value = ''
        for i in range(len(df)):
            if df['Word'][i] in syn_words:
                for j in range(i+1 ,i+10):
                    if df['POS tags'][j] == wordsPOS and df['POS tags'][j+1] == nextwordsPOS:
                        value += df['Word'][j]
                        value += df['Word'][j+1]
                    elif re.search(wordsNER, df['NER'][j]):
                        value += df['Word'][j]
                break
        return value

    def find_website(df, syn_words, wordsNER ):
        import re
        value = ''
        for i in range(len(df)):
            if df['Word'][i] in syn_words:
                    for j in range(i+1, i+10):
                        if re.search(wordsNER, df['NER'][j]):
                            value += df['Word'][j]
                    break
        return value

    def find_type_temple(df, syn_words = ['ประเภท', 'เป็น'] , words = 'วัด', nextword = 'ไทย', 
                        setofword_2_1 =['พระอารามหลวง', 'วัดราษฎร์','วัดหลวง'] , setofword_2_2 = ['ชั้นเอก', 'ชั้นโท', 'ชั้นตรี']
                        , words_2 = 'ชนิด' , setofword_2_3 = ['ราชวรมหาวิหาร', 'ราชวรวิหาร', 'วรมหาวิหาร', 'วรวิหาร', 'สามัญ']):
        value_type = ''
        # type
        for i in range(len(df)):
            if df['Word'][i] in syn_words:
                for j in range(i + 1, i + 10):
                    if df['Word'][j] == words :
                        value_type += df['Word'][j]
                        if df['Word'][j+1] == nextword :
                            value_type += df['Word'][j+1]
                        

                    elif df['Word'][j] in setofword_2_1:
                        value_type += df['Word'][j] + ' '
                        if df['Word'][j + 1] in setofword_2_2:
                            value_type += df['Word'][j + 1] + ' '
                            if df['Word'][j+2] == words_2:
                                value_type += df['Word'][j+2]
                                if df['Word'][j + 3] in setofword_2_3:
                                    value_type += df['Word'][j + 3] + ' '
                break

        return value_type

    def find_type(data_ner_pos, syn_words,  word_list,  POS_list = ['NCMN', 'RPRE']):
        value = ''
        for i in range(len(data_ner_pos)):
            if data_ner_pos['Word'][i] in syn_words:
                for x in range(i + 1, i + 2):
                    if data_ner_pos['Word'][x] in word_list:
                        value += data_ner_pos['Word'][x] 
                    elif data_ner_pos['POS tags'][x] in POS_list:
                        value += data_ner_pos['Word'][x] 
                break
                    
        return value

    def find_status_palace(df, syn_words, wordsPOS, wordsPOS_2, nextwordsPOS, isnotwords):
        import re
        value_status = ''
        # status
        for i in range(len(df)):
            if df['Word'][i] in syn_words:
                for j in range(i+1, i+3):
                    if re.search(wordsPOS, df['POS tags'][j]):
                        value_status += df['Word'][j]
                    elif df['POS tags'][j] == wordsPOS_2 and re.search(nextwordsPOS, df['POS tags'][j+1]):
                        value_status += df['Word'][j]
                    elif df['POS tags'][j] != isnotwords:
                        value_status += df['Word'][j]
                break
            
        return value_status

    def find_quantity(df, syn_words, POS_list , iswords , POSwords, NERwords):
        import re
        value = ''
        for i in range(len(df)):
                if df['Word'][i] in syn_words:
                    for j in range(i+1, i+10):
                        if df['POS tags'][j] in POS_list :
                            value += df['Word'][j] + ' '

                        elif df['Word'][j] == iswords or df['POS tags'][j] == POSwords:
                            value+= df['Word'][j] + ' '

                        elif re.search(NERwords , df['NER'][j]):
                            value +=df['Word'][j] + ' '
                    break
                
        return value

    def read_googlesheet(SHEETNAME):
        SHEET_ID = '1DGtkzyobGgcDD59man_nGt4rHOSsl8_ZiYg8_PDSDFw'
        SHEET_NAME = SHEETNAME
        url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
        rule = pd.read_csv(url)
        return(rule)

    def select_rule(name_rule, rule):
        rule = rule[rule['Rule'] == name_rule]
        rule_dict = rule.to_dict('records')
        dict = {}
        for item in rule_dict:
            for key, value in item.items():
                dict[key] = value
        return dict


    data = normalize(data)
    data_ner_pos = postag_ner(data)
    df = pd.DataFrame(data_ner_pos, columns=['Word', 'NER', 'POS tags'])
    infobox = {}

    if re.search(r'เป็นวัด|เป็นพระอารามหลวง', data) or df['Word'][0] in ['วัด']:
        # วัด
        rule = read_googlesheet('rule_Temple')
        dict = select_rule(name_rule_temple, rule = rule)
        
        value_location = extract_location(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF02']), dict['filterNextWord_inSynPOS_search_IF02_1'], dict['filterNextWord_inSynNER_isBeginTag_IF02_1_1'],
                                          dict['filterNextWord_inSynNER_isInsideTag_IF02_1_2'], dict['filterNextWord_inSynNER_search_IF02_1_3'],dict['filterNextWord_inSynWord_is_IF02_1_4'], 
                                            dict['filterNextWord_inSynNER_is_IF02_1_4'], dict['filterNextWord_inSynWord_is_IF02_1_5'], dict['filterNextWord_inSynPOS_nextis_IF02_1_5'],
                                            dict['filterNextWord_inSynPOS_is_IF02_1_6'])
        value_type = find_type_temple(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF01']), dict['filterNextWord_inSynWord_is_IF01_1'], dict['filterNextWord_inSynWord_nextwordis_IF01_1'],
                                      ast.literal_eval(dict['filterNextWord_inSynWord_secondwordisin_IF01_2']),dict['filterNextWord_inSynWord_thirdwordis_IF01_2'],
                                      ast.literal_eval(dict['filterNextWord_inSynWord_fourthwordisin_IF01_2'])) 
        value_sect = find_value_nextword(df, dict['filterNextWord_inSynPOS_search_IF03'], syn_words = ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF03']))

        infobox[syn_วัง['type'][0]] = value_type
        infobox[syn_วัด['location'][0]] = value_location
        infobox[syn_วัด['sect'][0]] = value_sect
    
    # พระราชวัง
    elif re.search(r'เป็นวัง|เป็นพระราชวัง', data) or df['Word'][0] in ['วัง', 'พระราชวัง']:
        rule = read_googlesheet('rule_Palace')
        dict = select_rule(name_rule_palace, rule = rule)
        
        value_type = find_type(df, ast.literal_eval(dict['filterNextWord_inSynWord_is_IF01_1']),ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF01']),ast.literal_eval(dict['filterNextWord_inSynPOS_in_IF01_2']))
        value_location = extract_location(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF02']), dict['filterNextWord_inSynPOS_search_IF02_1'], dict['filterNextWord_inSynNER_isBeginTag_IF02_1_1'],
                                          dict['filterNextWord_inSynNER_isInsideTag_IF02_1_2'], dict['filterNextWord_inSynNER_search_IF02_1_3'],dict['filterNextWord_inSynWord_is_IF02_1_4'], 
                                            dict['filterNextWord_inSynNER_is_IF02_1_4'], dict['filterNextWord_inSynWord_is_IF02_1_5'], dict['filterNextWord_inSynPOS_nextis_IF02_1_5'],
                                            dict['filterNextWord_inSynPOS_is_IF02_1_6'])
        value_status = find_status_palace(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF03']),dict['filterNextWord_inSynPOS_search_IF03_1'], 
                           dict['filterNextWord_inSynPOS_is_IF03_2'], dict['filterNextWord_inSynPOS_nextPOSsearchis_IF03_2'], dict['filterNextWord_inSynPOS_isnot_IF03_3'])
        value_city = find_value_nextword(df, dict['filterNextWord_inSynWord_is_IF04'], ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF04']))
        value_country = find_value_nextword(df, dict['filterNextWord_inSynWord_is_IF05'], ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF05']) )
        value_start_building = find_date(df, dict['filterNextWord_selectSetofsynWord_IF06'], dict['filterNextWord_inSynPOS_is_IF06'], dict['filterNextWord_inSynPOS_nextwordis_IF06'],dict['filterNextWord_inSynNER_search_IF06'])
        
        infobox[syn_วัง['type'][0]] = value_type
        infobox[syn_วัง['location'][0]] = value_location
        infobox[syn_วัง['status'][0]] = value_status
        infobox[syn_วัง['city'][0]] = value_city
        infobox[syn_วัง['country'][0]] = value_country
        infobox[syn_วัง['start building'][0]] = value_start_building

    # อุทยานแห่งชาติ
    elif re.search(r'เป็นอุทยานแห่งชาติ', data) or df['Word'][0] in ['อุทยานแห่งชาติ'] :
        rule = read_googlesheet('rule_Nationalpark')
        dict = select_rule(name_rule_nationalpark, rule = rule)


        value_location = extract_location(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF02']), dict['filterNextWord_inSynPOS_search_IF02_1'], dict['filterNextWord_inSynNER_isBeginTag_IF02_1_1'],
                                          dict['filterNextWord_inSynNER_isInsideTag_IF02_1_2'], dict['filterNextWord_inSynNER_search_IF02_1_3'],dict['filterNextWord_inSynWord_is_IF02_1_4'], 
                                            dict['filterNextWord_inSynNER_is_IF02_1_4'], dict['filterNextWord_inSynWord_is_IF02_1_5'], dict['filterNextWord_inSynPOS_nextis_IF02_1_5'],
                                            dict['filterNextWord_inSynPOS_is_IF02_1_6'])

        value_area = find_quantity(df,ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF01']),ast.literal_eval(dict['filterNextWord_inSynPOS_inlist_IF01']), dict['filterNextWord_inSynWord_is_IF01'],
                                        dict['filterNextWord_inSynPOS_is_IF01'], dict['filterNextWord_inSynNER_search_IF01'])

        value_government_agency = find_value_nextword_search(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF03']), dict['filterNextWord_inSynNER_search_IF03'])
        value_establish = find_date(df, dict['filterNextWord_selectSetofsynWord_IF04'], dict['filterNextWord_inSynPOS_is_IF04'], dict['filterNextWord_inSynPOS_nextwordis_IF04'],dict['filterNextWord_inSynNER_search_IF04'])
        value_coordinates = find_value_nextword_search(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF05']), dict['filterNextWord_inSynNER_search_IF05'])
                                
    
        infobox[syn_อุทยานแห่งชาติ['location'][0]] = value_location
        infobox[syn_อุทยานแห่งชาติ['area'][0]] = value_area
        infobox[syn_อุทยานแห่งชาติ['government agency'][0]] = value_government_agency
        infobox[syn_อุทยานแห่งชาติ['establish'][0]] = value_establish
        infobox[syn_อุทยานแห่งชาติ['coordinates'][0]] = value_coordinates

    # สถาบันอุดมศึกษา
    elif re.search(r'เป็นมหาวิทยาลัย|เป็นสถาบันอุดมศึกษา|ระดับอุดมศึกษา', data) or df['Word'][0] in ['มหาวิทยาลัย', 'วิทยาลัย', 'สถาบันการอาชีวศึกษา']:
        rule = read_googlesheet('rule_university')
        dict = select_rule(name_rule_university, rule = rule)

        value_type = find_type(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF01']),ast.literal_eval(dict['filterNextWord_inSynWord_in_IF01']),ast.literal_eval(dict['filterNextWord_inSynPOS_in_IF01']))

        value_website = find_website(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF03']), dict['filterNextWord_inSynNER_search_IF03'])

        value_location = extract_location(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF02']), dict['filterNextWord_inSynPOS_search_IF02_1'], dict['filterNextWord_inSynNER_isBeginTag_IF02_1_1'],
                                          dict['filterNextWord_inSynNER_isInsideTag_IF02_1_2'], dict['filterNextWord_inSynNER_search_IF02_1_3'],dict['filterNextWord_inSynWord_is_IF02_1_4'], 
                                            dict['filterNextWord_inSynNER_is_IF02_1_4'], dict['filterNextWord_inSynWord_is_IF02_1_5'], dict['filterNextWord_inSynPOS_nextis_IF02_1_5'],
                                            dict['filterNextWord_inSynPOS_is_IF02_1_6'])
                                            
        value_initials = find_value_nextword_search(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF04']), dict['filterNextWord_inSynNER_search_IF04'])

        value_establish = find_date(df, dict['filterNextWord_selectSetofsynWord_IF05'], dict['filterNextWord_inSynPOS_is_IF05'], dict['filterNextWord_inSynPOS_nextwordis_IF05'],dict['filterNextWord_inSynNER_search_IF05'])

        infobox[syn_สถาบันอุดมศึกษา['type'][0]] = value_type
        infobox[syn_สถาบันอุดมศึกษา['location'][0]] = value_location
        infobox[syn_สถาบันอุดมศึกษา['website'][0]] = value_website
        infobox[syn_สถาบันอุดมศึกษา['initials'][0]] = value_initials
        infobox[syn_สถาบันอุดมศึกษา['establish'][0]] = value_establish
    
    # โรงพยาบาล
    elif re.search(r'เป็นสถาบันการแพทย์|เป็นโรงพยาบาล', data) or df['Word'][0] in ['โรงพยาบาล', 'ศูนย์การแพทย์'] :
        rule = read_googlesheet('rule_hospital')
        dict = select_rule(name_rule_hospital, rule = rule)

        value_location = extract_location(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF02']), dict['filterNextWord_inSynPOS_search_IF02_1'], dict['filterNextWord_inSynNER_isBeginTag_IF02_1_1'],
                                          dict['filterNextWord_inSynNER_isInsideTag_IF02_1_2'], dict['filterNextWord_inSynNER_search_IF02_1_3'],dict['filterNextWord_inSynWord_is_IF02_1_4'], 
                                            dict['filterNextWord_inSynNER_is_IF02_1_4'], dict['filterNextWord_inSynWord_is_IF02_1_5'], dict['filterNextWord_inSynPOS_nextis_IF02_1_5'],
                                            dict['filterNextWord_inSynPOS_is_IF02_1_6'])

        value_type = find_type(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF01']),ast.literal_eval(dict['filterNextWord_inSynWord_in_IF01']),ast.literal_eval(dict['filterNextWord_inSynPOS_in_IF01']))
    
        value_number_beds = find_quantity(df,ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF03']),ast.literal_eval(dict['filterNextWord_inSynPOS_inlist_IF03']), dict['filterNextWord_inSynWord_is_IF03'],
                                        dict['filterNextWord_inSynPOS_is_IF03'], dict['filterNextWord_inSynNER_search_IF03'])
        

        value_website = find_website(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF04']), dict['filterNextWord_inSynNER_search_IF04'])
        
        value_affiliation = find_value_nextword_search(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF05']), dict['filterNextWord_inSynNER_search_IF05'])

        
        infobox[syn_โรงพยาบาล['type'][0]] = value_type  
        infobox[syn_โรงพยาบาล['location'][0]] = value_location     
        infobox[syn_โรงพยาบาล['number of beds'][0]] = value_number_beds
        infobox[syn_โรงพยาบาล['website'][0]] = value_website
        infobox[syn_โรงพยาบาล['affiliation'][0]] = value_affiliation
        

    # default
    else:
        rule = read_googlesheet('rule_default')
        dict = select_rule(name_rule_default, rule = rule)

        value_location = extract_location(df, ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF02']), dict['filterNextWord_inSynPOS_search_IF02_1'], dict['filterNextWord_inSynNER_isBeginTag_IF02_1_1'],
                                          dict['filterNextWord_inSynNER_isInsideTag_IF02_1_2'], dict['filterNextWord_inSynNER_search_IF02_1_3'],dict['filterNextWord_inSynWord_is_IF02_1_4'], 
                                            dict['filterNextWord_inSynNER_is_IF02_1_4'], dict['filterNextWord_inSynWord_is_IF02_1_5'], dict['filterNextWord_inSynPOS_nextis_IF02_1_5'],
                                            dict['filterNextWord_inSynPOS_is_IF02_1_6'])
        value_type = ''
        value_name = ''
        value_Related_person = ''

        for i in range(len(df)):
        # name and type
            if df['Word'][i] in ast.literal_eval(dict['filterNextWord_selectSetofsynWord_IF01']):
                if df['Word'][i] == dict['filterNextWord_inSynWord_is_IF01']:
                    # ชื่อ
                    for j in range(0, i):
                        if re.search(dict['filterNextWord_inSynPOS_search_IF01'], df['POS tags'][j]):
                            value_name = df['Word'][j] + ' '
                            break
                    for j in range(i, i+2):
                        if re.search(dict['filterNextWord_inSynPOS_search_IF01'], df['POS tags'][j]):
                            value_type = df['Word'][j] + ' '
                            break
                    break

            #value_Related_person
            else :
                if re.search(dict['filterNextWord_inSynNER_search_IF01'], df['NER'][i]):
                    value_Related_person += df['Word'][i]

        infobox[syn_default['name'][0]] = value_name
        infobox[syn_default['type'][0]] = value_type
        infobox[syn_default['location'][0]] = value_location
        infobox[syn_default['Related person'][0]] = value_Related_person
    
    return infobox

