# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 11:53:36 2019

@author: payam.bagheri
"""
# this loop finds the (condensed) unique words in the data and stores their frequency in a dictionary
# the unique words list is a condensed list, i.e. different words that are "too" similar to each other
# are represented by the one word.

all_data = pd.read_excel(dir_path + '/0_input_data/messaging-open-end-all-quarters-english-cleaned.xlsx')
#all_data = shuffle(all_data, random_state=0)
data_raw = all_data.copy()

unique_words_freq_dic = defaultdict(dict)
unique_words = ['notawordbyitself']
for ind in tqdm(data_raw.index):
    st = data_raw['aw_unaided_ad_message'][ind]
    if isNaN(st):
        st = 'isnan'
    st = mess_prep(data_raw['aw_unaided_ad_message'][ind])
    for w in st:
        #print(w)
        is_unique = [(similar(w.lower(), x), x) for x in unique_words]
        is_unique = sorted(is_unique, key=takeFirst, reverse=True)
        if is_unique[0][0] < 0.7:
            #print(ind)
            unique_words.append(w.lower())
            unique_words_freq_dic[w.lower()][data_raw['aw_unaided_ad_message_en_sroec1'][ind]] = 1
        else:
            try:
                unique_words_freq_dic[is_unique[0][1]][data_raw['aw_unaided_ad_message_en_sroec1'][ind]] += 1
            except KeyError:
                unique_words_freq_dic[is_unique[0][1]][data_raw['aw_unaided_ad_message_en_sroec1'][ind]] = 1
               
len(unique_words)


unique_words_freq_dic_pickle = dir_path + '/0_input_data/unique_words_freq_dic.pickle'
pickle_out = open(unique_words_freq_dic_pickle,"wb")
pickle.dump(unique_words_freq_dic, pickle_out)
pickle_out.close()




# creating a new column that contains a condensed version of the text responses where words are replaced by the
# most similar word from the list of the condensed unique words created above.
data_raw['aw_unaided_ad_message_dense'] = np.nan
for ind in tqdm(data_raw.index):
    mes = data_raw['aw_unaided_ad_message'][ind]
    prep_mess = mess_prep(mes)
    dense_st = [] # this is a new version of each message were words are replaced by their most similar from unique_words
    for wor in prep_mess:
        #print(wor)
        sims = [(similar(wor, x), x) for x in unique_words]
        sim = sorted(sims, key=takeFirst, reverse=True)
        sim_wor = sim[0][1]
        dense_st.append(sim_wor)
    data_raw['aw_unaided_ad_message_dense'][ind] = dense_st
        #print(sim_wor)


# joining words to make a sentense
data_raw['aw_unaided_ad_message_dense'] = data_raw['aw_unaided_ad_message_dense'].apply(lambda x: str_join(x))

data_raw.columns

data_raw.to_csv(dir_path + '/0_input_data/bigfoot/bigfoot_message_dense_data.csv', index=False)

