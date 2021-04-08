import json
import pandas as pd
import numpy as np
import os


# Reads data file names from structured directory (data files
def read_file_names(directory_1):

    final_data_list = []

    directory_1_list = os.listdir(directory_1)

    for path_1 in directory_1_list:

        directory_2 = directory_1 + "/" + path_1  # ['data/data1]

        directory_2_list = os.listdir(directory_2)  # ['DiseaseOrSyndrome']

        for path_2 in directory_2_list:

            directory_3 = directory_2 + "/" + path_2

            directory_3_list = os.listdir(directory_3)

            xlsx_list = []
            existing_pairs = []
            final_tuple_list = []

            if len(directory_3_list) == 1:

                entry_split = directory_3_list[0].split('_')

                entry_properties = {"source_node_id": entry_split[3].replace("Source=", ""),
                                    "target_CUI": entry_split[5].replace("Target=", ""),
                                    "type": entry_split[4],
                                    "name": entry_split[6].replace(".xlsx", "")}

                xlsx_path_entry = directory_3 + "/" + directory_3_list[0]

                entry_final = {"xlsx_path": xlsx_path_entry, "target_node_properties": entry_properties}

                final_tuple_list.append([entry_final])

                final_data_list.append(final_tuple_list)

            else:

                for file in directory_3_list:
                    if ".xlsx" not in file:
                        pass
                    else:
                        xlsx_list.append(file)

                for entry in xlsx_list:

                    for target in xlsx_list:

                        if entry == target:
                            pass

                        elif (entry, target) in existing_pairs:
                            pass

                        elif (target, entry) in existing_pairs:
                            pass

                        else:

                            entry_split = entry.split('_')

                            target_split = target.split('_')

                            entry_properties = {"source_node_id": entry_split[3].replace("Source=", ""),
                                                "target_CUI": entry_split[5].replace("Target=", ""),
                                                "type": target_split[4],
                                                "name": entry_split[6].replace(".xlsx", "")}
                            target_properties = {"source_node_id": entry_split[3].replace("Source=", ""),
                                                 "target_CUI": target_split[5].replace("Target=", ""),
                                                 "type": target_split[4],
                                                 "name": target_split[6].replace(".xlsx", "")}

                            xlsx_path_entry = directory_3 + "/" + entry
                            xlsx_path_target = directory_3 + "/" + target

                            entry_final = {"xlsx_path": xlsx_path_entry, "target_node_properties": entry_properties}
                            target_final = {"xlsx_path": xlsx_path_target, "target_node_properties": target_properties}

                            temporary_tuple = (entry_final, target_final)

                            final_tuple_list.append(temporary_tuple)

                            existing_pairs.append((entry, target))

                final_data_list.append(final_tuple_list)

    return final_data_list


# Converts xlsx file to pandas dataframe
def xlsx_to_df(path):

    df = pd.read_excel(path)

    df.rename(columns={'Unnamed: 0': 'source_node'}, inplace=True)

    return df


# Adds target node to respective pandas dataframe (each SemNet simulation requires one target node per output)
def add_targets(df, target):

    target_node_list = []

    for z in range(len(df.index)):
        target_node_list.append(target)

    df[target] = target_node_list

    return df


# Normalizes relative hetesim set to values between 0 and 1 (zero being most relevant, 1 being least)
def hetesim_normalize(df_hetesim, df, tn):

    df['hetesim'].astype(float)

    min_hetesim = df['hetesim'].min()

    max_hetesim = df['hetesim'].max()

    hetesim_difference = max_hetesim - min_hetesim

    df['hetesim_normalized'] = (df['hetesim'] - min_hetesim) / hetesim_difference

    em_list = []

    for row in df.iterrows():
        em_list.append(row[1]['source_node'])

    for row in em_list:

        if row in df_hetesim['source_node'].values:

            pass

        else:

            df_hetesim = df_hetesim.append({'source_node': row}, ignore_index=True)

    for row in df.iterrows():

        local_df_sn = row[1]['source_node']

        local_df_normal_hetesim = row[1]['hetesim_normalized']

        global_sn_index = df_hetesim.loc[df_hetesim['source_node'] == local_df_sn].index[0]

        if ('hetesim_normalized_TN_' + tn) not in df_hetesim:

            df_hetesim['hetesim_normalized_TN_' + tn] = np.nan

        df_hetesim.loc[global_sn_index, 'hetesim_normalized_TN_' + tn] = local_df_normal_hetesim

    return df_hetesim, df


# Averages the normalized hetesim scores of the two datasets
# (where they share source nodes and have different target nodes; can only be two) - this function is less important
def hetesim_average(df_1, df_2, sn, tn_1, tn_2):

    'csv_dump'

    df_2 = df_2.sort_values('source_node')

    hetesim_average_list = []
    em_list = []
    em_list2 = []

    for row in df_1.iterrows():
        em_list.append(row[1]['hetesim_normalized'])

    for row in df_2.iterrows():
        em_list2.append(row[1]['hetesim_normalized'])

    if len(df_1.index) != len(df_2.index):
        print("ERROR IN HETESIM AVG: DATAFRAMES ARE NOT COMPATIBLE")

    for row in range(len(df_1.index)):
        hetesim_average_list.append((em_list[row] + em_list2[row]) / 2)

    df_1['hetesim_avg' + '_SN_' + sn + '_TN1_' + tn_1 + '_TN2_' + tn_2] = hetesim_average_list
    df_2['hetesim_avg' + '_SN_' + sn + '_TN1_' + tn_2 + '_TN2_' + tn_1] = hetesim_average_list

    return df_1, df_2


# Finds top X percent of average hetesim scores shared between two datasets (needs further implementation)
def top_hetesim_average(df, sn, tn_1, tn_2, percent):

    df = df.sort_values('hetesim_avg' + '_SN_' + sn + '_TN1_' + tn_1 + '_TN2_' + tn_2)

    length = len(df.index)
    top_x_percent = round(length * percent)

    em_list = []
    count = 0

    for row in df.iterrows():

        em_list.append((row[1]['source_node'], row[1]['hetesim_avg' + '_SN_' + sn + '_TN1_' + tn_1 + '_TN2_' + tn_2]))

        count = count + 1

        if count == top_x_percent:
            break

    return em_list


# Adds source nodes to node list (checks for duplicates)
def generate_nodes(node_list, df, sn):

    df.sort_index(inplace=True)

    em_list = []

    for i in node_list:
        em_list.append(i['id'])

    for row in df.iterrows():

        if (row[1]['source_node']  + ' linked with ' + sn) in em_list:

            pass

        else:

            # Eventually implement count feature
            empty_dict = {'id': (row[1]['source_node'] + ' linked with ' + sn),
                          'name': row[1]['source_node'],
                          'kind': row[1]['kind'],
                          'node_group': sn,
                          'node_type': 'source_node'}

            node_list.append(empty_dict)

    return node_list


# Adds target nodes to node list (checks for duplicates)
def generate_target_nodes(node_list, tn_combined):

    for target_node in tn_combined:

        em_list = []

        for i in node_list:
            em_list.append(i['id'])

        if tn_combined[target_node]['target_CUI'] in em_list:

            pass

        else:
            empty_dict = {'id': tn_combined[target_node]['target_CUI'],
                          'name': tn_combined[target_node]['name'],
                          'node_group': tn_combined[target_node]['target_CUI'],
                          'node_type': 'target_node'}

            node_list.append(empty_dict)

    return node_list


# Adds links to node list (checks for duplicates)
def generate_links(link_list, df_1, df_2, sn, t1, t2):

    df_1 = df_1.sort_values('source_node')

    em_list = []

    for i in link_list:
        em_list.append((i['source'], i['target']))

    for row in df_1.iterrows():

        if ((row[1]['source_node'] + ' linked with ' + sn), row[1][t1]) in em_list:

            pass

        else:

            empty_dict = {'source': (row[1]['source_node'] + ' linked with ' + sn),
                          'target': (row[1][t1]),
                          'hetesim': float(row[1]['hetesim']),
                          'hetesim_normalized': float(row[1]['hetesim_normalized'])}

            link_list.append(empty_dict)

    if df_2 is not None:

        df_2 = df_2.sort_values('source_node')

        em_list_2 = []

        for i in link_list:
            em_list_2.append((i['source'], i['target']))

        for row in df_2.iterrows():

            if ((row[1]['source_node'] + ' linked with ' + sn), row[1][t2]) in em_list_2:

                pass

            else:

                empty_dict = {'source': (row[1]['source_node'] + ' linked with ' + sn),
                              'target': row[1][t2],
                              'hetesim': float(row[1]['hetesim']),
                              'hetesim_normalized': float(row[1]['hetesim_normalized'])}

                link_list.append(empty_dict)

    return link_list


# Unites normalized hetesim scores for each unique source node
def add_global_hetesim(node_list, df_hetesim):

    df_hetesim['avg_global_hetesim'] = np.nan

    col_list = []

    for col in df_hetesim.columns:
        col_list.append(col)

    for row in df_hetesim.iterrows():

        count_1 = 0

        normalized_sum = 0
        normalized_denom = 0

        for column in col_list:

            if (count_1 > 0) & (count_1 < (len(df_hetesim.columns) - 1)):

                if df_hetesim.at[row[0], column] != np.nan:

                    normalized_sum = normalized_sum + df_hetesim.at[row[0], column]
                    normalized_denom = normalized_denom + 1

            count_1 = count_1 + 1

        df_hetesim.loc[row[0], "avg_global_hetesim"] = normalized_sum / normalized_denom

    for node in range(len(node_list)):

        if node_list[node]['node_type'] != 'target_node':

            temp_sn = node_list[node]['name']

            df_hetesim_index = df_hetesim.loc[df_hetesim['source_node'] == temp_sn].index[0]

            node_list[node]['avg_global_hetesim'] = df_hetesim.at[df_hetesim_index, 'avg_global_hetesim']

    return node_list, df_hetesim


# Generates the json output (taking in node_list and link_list to follow 3D-graph format)
def generate_json(path, node_list, link_list):

    final_dict = {"nodes": node_list, "links": link_list}

    with open(path, "w") as json_file:
        json_file.write(json.dumps(final_dict, indent=4))


# Generates a csv from dataframe
def generate_csv(df, path):

    df = df.sort_values('avg_global_hetesim')

    df.to_csv(path)

    return path


# Generates a xlsx from dataframe
def generate_xlsx(df, path):

    df = df.sort_values('avg_global_hetesim')

    df.to_excel(path)

    return path


# Combines above functions to generate the final json output
def bring_it_together(data_list, node_list, link_list):

    target_node_information = {}
    target_count = 0

    for tuple_list in data_list:

        global_hetesim_dataframe = pd.DataFrame()
        global_hetesim_dataframe['source_node'] = None

        sub_node_list = []
        sub_link_list = []

        source_node_type = None

        for pair in tuple_list:

            if len(pair) == 1:

                target_node_properties = pair[0]['target_node_properties']  # source nodes in respect to target 1

                target_node = {'target_1': target_node_properties}

                for target_node_entries in target_node:
                    target_node_information['target' + str(target_count)] = target_node[target_node_entries]

                    target_count = target_count + 1

                id_a = target_node_properties['target_CUI']

                source_node_id = target_node_properties['source_node_id']

                source_node_type = target_node_properties['type']

                xlsx_path = pair[0]['xlsx_path']

                dataframe_1 = xlsx_to_df(xlsx_path)

                dataframe_1 = add_targets(dataframe_1, id_a)

                hetesin_adj = hetesim_normalize(global_hetesim_dataframe, dataframe_1, id_a)
                global_hetesim_dataframe = hetesin_adj[0]
                dataframe_1 = hetesin_adj[1]

                generate_nodes(sub_node_list, dataframe_1, source_node_id)

                generate_links(sub_link_list, dataframe_1, None, source_node_id, id_a, None)

            else:

                target_node_properties_1 = pair[0]['target_node_properties']  # source nodes in respect to target 1
                target_node_properties_2 = pair[1]['target_node_properties']  # source nodes in respect to target 2

                target_nodes_combined = {'target_1': target_node_properties_1, 'target_2': target_node_properties_2}

                for target_node_entries in target_nodes_combined:

                    target_node_information['target' + str(target_count)] = target_nodes_combined[target_node_entries]

                    target_count = target_count + 1

                id_a = target_node_properties_1['target_CUI']
                id_b = target_node_properties_2['target_CUI']

                source_node_id = target_node_properties_1['source_node_id']

                source_node_type = target_node_properties_1['type']

                xlsx_path_1 = pair[0]['xlsx_path']
                xlsx_path_2 = pair[1]['xlsx_path']

                dataframe_1 = xlsx_to_df(xlsx_path_1)

                dataframe_2 = xlsx_to_df(xlsx_path_2)

                dataframe_1 = add_targets(dataframe_1, id_a)

                dataframe_2 = add_targets(dataframe_2, id_b)

                hetesin_adj = hetesim_normalize(global_hetesim_dataframe, dataframe_1, id_a)
                global_hetesim_dataframe = hetesin_adj[0]
                dataframe_1 = hetesin_adj[1]

                hetesin_adj = hetesim_normalize(global_hetesim_dataframe, dataframe_2, id_b)
                global_hetesim_dataframe = hetesin_adj[0]
                dataframe_2 = hetesin_adj[1]

                avg_hetesim = hetesim_average(dataframe_1, dataframe_2, source_node_id, id_a, id_b)
                dataframe_1 = avg_hetesim[0]
                dataframe_2 = avg_hetesim[1]

                generate_nodes(sub_node_list, dataframe_1, source_node_id)

                generate_links(sub_link_list, dataframe_1, dataframe_2, source_node_id, id_a, id_b)

        global_hetesim_output = add_global_hetesim(sub_node_list, global_hetesim_dataframe)

        sub_node_list = global_hetesim_output[0]

        global_hetesim_dataframe = global_hetesim_output[1]

        if not os.path.exists('csv_dump'):
            os.makedirs('csv_dump')

        if not os.path.exists('xlsx_dump'):
            os.makedirs('xlsx_dump')

        generate_xlsx(global_hetesim_dataframe, 'xlsx_dump/global_xlsx_{sn}_{snt}.xlsx'.format(sn=tuple_list[0][0]['target_node_properties']['source_node_id'], snt=source_node_type))

        # generate_csv(global_hetesim_dataframe, 'csv_dump/global_csv_{snt}'.format(snt=source_node_type))

        for sub_node in sub_node_list:
            node_list.append(sub_node)

        for sub_link in sub_link_list:
            link_list.append(sub_link)

    generate_target_nodes(node_list, target_node_information)

    generate_json(json_path, node_list, link_list)

    return node_list, link_list


# Main - important! Specify path to organized data folders in read_file_names()
if __name__ == '__main__':

    dataset_pair_list = read_file_names('test-data')

    json_path = 'nodes_links_output.json'

    csv_path = 'nodes_links_output.csv'

    nodes = []
    links = []

    nodes_links = bring_it_together(dataset_pair_list, nodes, links)
