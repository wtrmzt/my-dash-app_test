import dash
from dash import dcc, html, Input, Output, State
import visdcc
import pandas as pd
import networkx as nx
from openai import OpenAI
import re
import ast
import os

app = dash.Dash(__name__)
api_key = os.getenv("OPENAI_API_KEY")

# CSVデータの読み込み
def load_csv_data(subjectname):
    nodes_file = './subject_maps/subject_map_'+ subjectname +'_nodes.csv'  # CSVファイルのパス
    edges_file = './subject_maps/subject_map_'+subjectname+'_edges.csv'
    nodes = []
    edges = []
    if subjectname=='リセット':
        return nodes,edges
    nodes_df = pd.read_csv(nodes_file)
    for index, row in nodes_df.iterrows():
        nodes.append({'id': row['id'], 'label': row['label'], 'color': row['color']})

    edges_df = pd.read_csv(edges_file)
    for index, row in edges_df.iterrows():
        edges.append({'from': row['from'], 'to': row['to']})

    return nodes, edges

# CSVデータの読み込み
def relate_map(nodes, edges):
    #new_nodes = [{'id': node['id'], 'label': f"Modified {node['label']}"} for node in nodes]
    node_name=nodes[0]['label']
    subject_name=nodes[0]['id']
    print('node'+node_name)
    print('subject'+subject_name)
    new_map = text2dic(relate_GPToutput(node_name),subject_name)
    new_map = rename_id_added(new_map,subject_name)
    #node_name=nodes['label']
    return new_map
def reflection_map(text):
    subject_name='振り返り'
    new_map = text2dic(relate_GPToutput(text),subject_name)
    new_map = rename_id(new_map,subject_name)
    return new_map
def relate_GPToutput(input_name):
    node_gpt_output=[]
    OpenAI.api_key = api_key
    res = OpenAI.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''#命令
    あなたは優秀な教員です。以下の条件に従い、最善の出力をしてください。'''},  # 役割設定
                {"role": "user", "content": '''
    #条件
    入力として、単元名が1つ与えられる。これを基に関連項目を示すように知識マップを作成する。知識マップ作成の条件は、以下である。
    ・中心のノードは単元名。
    ・高さ1の知識マップを作成。
    ・それぞれのノードに対して、記述を基にして140字以内で説明文を生成せよ。
    ・学習するにあたってその単元を深める項目であること

    #出力
    PythonのNetworkXライブラリで読み込み可能な、nodes辞書と、edges辞書の2つ。
    ・nodes=[{'id':i,'label':"node_name",'sentence':"writetext"}]：ノードが格納される。idにはノードの番号を格納。labelにはノード名、sentenceには説明文を140字以内で格納する。

    ・edges=[{'from':node_id,'to':node_id}]：fromにはエッジの始点のノードid、toにはエッジの終点のノードidを格納する。
    ・これ以外は必要ない。

    #入力
                '''+input_name}               # 最初の質問
            ],
            temperature=0.0  # 温度（0-2, デフォルト1）
        )
    node_gpt_output.append(res.choices[0].message.content)
    return node_gpt_output
def clean_list_comments(input_str):
    # 正規表現パターン定義
    pattern = re.compile(r'\[.*?\]', re.DOTALL)
    
    # リスト部分を全て取得
    lists = pattern.findall(input_str)
    
    cleaned_lists = []
    
    for lst in lists:
        # # から始まる行を削除
        lst_cleaned_comments = re.sub(r'#.*?\n', '', lst)
        
        # ] の前にある , を削除
        lst_cleaned_comma = re.sub(r',\s*]', ']', lst_cleaned_comments)
        
        cleaned_lists.append(lst_cleaned_comma)
    
    # 元の文字列にクリーンなリストを置き換える
    for original, cleaned in zip(lists, cleaned_lists):
        input_str = input_str.replace(original, cleaned)
    
    return input_str
def text2dic(node_gpt_output,subject_name):
    node_gpt_map=[]
    for i in range(len(node_gpt_output)):
        # 正規表現でノードとエッジの部分を抽出
        nodes_pattern = re.compile(r'nodes = \s*(\[\s*\{.*?\}\s*\])', re.DOTALL)
        edges_pattern = re.compile(r'edges = \s*(\[\s*\{.*?\}\s*\])', re.DOTALL)
        #print('nodes'+node_gpt_output[i])
        nodes_match = nodes_pattern.search(clean_list_comments(node_gpt_output[i]))
        edges_match = edges_pattern.search(clean_list_comments(node_gpt_output[i]))

        if nodes_match:
            nodes_str = nodes_match.group(1)
            nodes = ast.literal_eval(nodes_str)
        else:
            #print(i)
            print("Nodes情報が見つかりませんでした。")

        if edges_match:
            edges_str = edges_match.group(1)
            edges = ast.literal_eval(edges_str)
        else:
            #print(i)
            print("Edges情報が見つかりませんでした。")
            #print(nodes)
        node_gpt_map.append({'nodes':nodes,'edges':edges,'subject':subject_name})
    #print(node_gpt_map)
    #node_gpt_map=rename_id_added(node_gpt_map,subject_name)
    #print(node_gpt_map)

    return node_gpt_map
def rename_id_added(map,name):
    color = "#FFE568"
    map=map[0]
    root = map['nodes'][0]['id']
    map['nodes'][0]['id'] = name# +'_'+str(map['nodes'][0]['id'])
    map['nodes'][0]['color']=color
    print(map)
    for i in range(1,len(map['nodes'])):
        map['nodes'][i]['id'] = name + '_' + str(map['nodes'][i]['id']) 
        map['nodes'][i]['color'] = color

    for j in range(len(map['edges'])):
        if map['edges'][j]['from'] == root:
            map['edges'][j]['from'] = name# + '_' + str(map['edges'][j]['from'])
            map['edges'][j]['to'] = name + '_' + str(map['edges'][j]['to'])
        elif map['edges'][j]['to'] == root:
            map['edges'][j]['from'] = name + '_' + str(map['edges'][j]['from'])
            map['edges'][j]['to'] = name# + '_' + str(map['edges'][j]['to'])
        else:
            map['edges'][j]['from'] = name + '_' + str(map['edges'][j]['from'])
            map['edges'][j]['to'] = name + '_' + str(map['edges'][j]['to'])
    return map
def rename_id(map,name):
    print(map)
    map=map[0]
    color = {'情報I':'#A0D8EF','コンピューターリテラシー':'#F8C6BD','プログラミング通論':'#E3EBA4','美術A':'#FFFFFF','振り返り':'#FFFFFF'}
    for i in range(len(map['nodes'])):
        map['nodes'][i]['id'] = name + '_' + str(map['nodes'][i]['id'])
        map['nodes'][i]['color'] = color[name]
    for j in range(len(map['edges'])):
        map['edges'][j]['from'] = name + '_' + str(map['edges'][j]['from'])
        map['edges'][j]['to'] = name + '_' + str(map['edges'][j]['to'])
    return map
def reflection_GPToutput(input_text):
    OpenAI.api_key = api_key
    node_gpt_output=[]
    res = OpenAI.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''#命令
    あなたは優秀な教員です。以下の条件に従い、最善の出力をしてください。'''},  # 役割設定
                {"role": "user", "content": '''
#条件
入力に生徒の振り返り記述の内容が書かれる。この記述を基に、"分野ごと"に木を伸ばす知識マップを作成しなさい。
・それぞれのノードに対して、140字以内で説明文を生成せよ。
・ルートノードは、振り返り単元である。
・「課題」・「演習」などのノードは使用しない
・ノード名は簡潔にせよ
・高さは自由である．必要に応じて伸ばして良い
・作成した木を見返してもいいように、'学習の理解を深める体系的な内容のみ'であること。
    #出力
    PythonのNetworkXライブラリで読み込み可能な、nodes辞書と、edges辞書の2つ。
    ・nodes=[{'id':i,'label':"node_name",'sentence':"writetext"}]：ノードが格納される。idにはノードの番号を格納。labelにはノード名、sentenceには説明文を140字以内で格納する。

    ・edges=[{'from':node_id,'to':node_id}]：fromにはエッジの始点のノードid、toにはエッジの終点のノードidを格納する。
    ・これ以外は必要ない。

    #入力
                '''+input_text}               # 最初の質問
            ],
            temperature=0.0  # 温度（0-2, デフォルト1）
        )
    node_gpt_output.append(res.choices[0].message.content)
    return node_gpt_output




def similar_add_edge(map1, map2):
    # マップ間の類似度計算とエッジの追加（ダミーデータ）
    new_edges = map1['edges'] + [{'from': node['id'], 'to': node['id']} for node in map2['nodes']]

    

    return {'nodes': map1['nodes'] + map2['nodes'], 'edges': new_edges}

# 初期ノードとエッジのデータ
dropdown_list = ['コンピューターリテラシー','プログラミング通論', '情報I','リセット']
initial_nodes, initial_edges = load_csv_data('コンピューターリテラシー')
#for sub in subject_list:
#    tmp_nodes, tmp_edges = load_csv_data(sub)
#    initial_nodes.extend(tmp_nodes)
#    initial_edges.extend(tmp_edges)

app.layout = html.Div([
    html.Div(style={'width': '5%', 'height': '100vh', 'backgroundColor': '#4285f4', 'float': 'left'}),
    html.Div([
        html.Div([
            html.H3('マップの表示1', style={'padding': '10px'}),
            dcc.Dropdown(
                id='dropdown-selection_map',
                options=[
                    {'label': dropdown_list[i], 'value': i} for i in range(0, 4)
                ],
                placeholder='マップが選択できます'
            ),
            visdcc.Network(
                id='net',
                data={'nodes': initial_nodes, 'edges': initial_edges},
                options={
                    'height': '800px', 'width': '100%',
                    'clickToUse': True,
                    'physics': {'barnesHut': {'avoidOverlap': 0}},
                },
                selection={'nodes': [], 'edges': []}
            )
        ], style={'width': '47%', 'height': '90vh', 'float': 'left', 'border': '1px solid black', 'border-radius': '10px', 'padding': '10px', 'margin': '5px'}),
        html.Div([
            html.Div([
                html.H3('1で選択されたノードの表示', style={'padding': '10px'}),
                html.Div(id='selected-node-info', style={'padding': '10px'}),
                visdcc.Network(
                    id='selected-net',
                    data={'nodes': [], 'edges': []},
                    options={
                        'height': '400px', 'width': '100%',
                        'clickToUse': True,
                        'physics': {'barnesHut': {'avoidOverlap': 0}},
                    }
                )
            ], style={'width': '48%', 'height': '50vh', 'float': 'left', 'border': '1px solid black', 'border-radius': '10px', 'padding': '10px', 'margin': '2px'}),
            html.Div([
                html.H3('ノード名', style={'padding': '10px'}),
                html.Div(id='text-display', style={'padding': '10px'}),
                html.H3('説明', style={'padding': '10px'}),
                html.Div(id='sentence-display', style={'padding': '10px'}),
                html.Button('グラフ生成', id='generate-graph-button', n_clicks=0, style={'margin-left': '10px'}),
                html.Button('反映', id='reflect-changes-button', n_clicks=0, style={'margin-left': '10px'}),
                html.Button('類似度計算', id='similarity-button', n_clicks=0, style={'margin-left': '10px'})
            ], style={'width': '45%', 'height': '50vh','float': 'right', 'border': '1px solid black', 'border-radius': '10px', 'padding': '10px', 'margin': '2x'}),
        ], style={'width': '50%', 'float': 'right'}),

        html.Div([
            html.H3('振り返り', style={'padding': '10px'}),
            dcc.Dropdown(
                id='dropdown-selection',
                options=[
                    {'label': f'Sample{i}', 'value': i} for i in range(1, 6)
                ],
                placeholder='テキストを選択してください'
            ),
            dcc.Textarea(
                id='textarea-input',
                style={'width': '100%', 'height': 200},
                placeholder='ここにテキストを入力してください...',
            ),
            html.Button('追加', id='add-button', n_clicks=0, style={'margin-left': '10px'}),
        ], style={'width': '48%', 'height': '36vh','float': 'right', 'border': '1px solid black', 'border-radius': '10px', 'padding': '10px', 'margin': '2px'})
    ], style={'width': '95%', 'float': 'left'}),
    dcc.Loading(
        id="loading",
        type="dot",
        overlay_style={"visibility":"visible", "filter": "blur(2px)"},
        children=html.Div(id="loading-output"),
        style={'position': 'fixed', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)'}
    )
])
@app.callback(
    Output('textarea-input', 'value'),
    Input('dropdown-selection', 'value')
)
def update_textarea(selected_text):
    if selected_text==None:
        return ''
    sample_list=[
        '''dateコマンドのマニュアルに”that”の文字が一つも使われていないことが分かったが、一方、”this”の文字は1回のみ使われていた。したがってマニュアルの内容に指示語が多用されていないことが分かった。
また、測定に際しtrとsortを用いて順番に並べると長くなってしまうため、同様の検証をまた行う際にはheadやtailを用いて表示する件数を少なくする工夫をするとコンピュータに負担がかからない測定ができると考える。
''',
'''測定結果より次の事実を得る。大文字小文字の区別の有無に違いによってisの文字数に増減がないことから疑問文” Is ~?”　の文は無い。マニュアルであるため疑問文は無いのは直感に従う。また、”e”,”g”の単体の文字が数回使われている。これは、e.g.の表現で「例えば」という意味を持つため、文字単体で複数回使用されていると考えられる。
''',
'''まず、凍結させてから、再開するまで時計の挙動を観察すると、再開した際に即座に現在の時刻の位置に針が移動し現在の時刻を示すようになった。
また、プログラムを-TERMと-KILLで終了させたとき、この2つの違いは特にみられなかった。しかしインターネットで強制終了について調べると、最悪の場合OSのが破損する可能性があるという記述を見つけたため強制終了のコマンドは多用するべきではない。
参考：https://pc-farm.co.jp/pc_column/pc/2284/
''',
'''結果より、サイズの辺の大きさが2倍になると、そのファイルサイズも2倍になる。また、黒色が使われている画像の方がややファイルサイズが大きいことが分かった。
ここから考えられることは、Gimpでの加工の量によってファイルサイズが決まるのではないかということだ。画面全体に大きな絵を書くことによって大きなサイズであればあるほどファイルサイズが大きくなり、背景を黒として画面すべて加工することによってややファイルサイズが大きくなることと考える。
''',
'''私が知ったことは大きく分けて2つある。1つは、マウスによるファイル操作との比較である。2つ目は、処理速度の速さである。1つ目について、マウス操作でも同様の動作ができるものの手間自体はそんなに変わらない。しかし、保護モードを変更する作業などにいおいてはUnixシステムが優れている。2つ目について、通常では1つのファイルをコピーする際コピーに1秒弱かかってしまう。しかしUnixシステムは実行を行った直後にコピーされる。処理速度の速さはUnixシステムの強みであるといえるかもしれない。'''
    ]
    return sample_list[selected_text-1]

@app.callback(
    Output('net', 'data', allow_duplicate=True),
    Output('selected-node-info', 'children'),
    Output('text-display', 'children'),
    Output('selected-net', 'data'),
    Input('net', 'selection'),
    State('net', 'data'),
    prevent_initial_call=True
)
def update_selection(selection, net_data):
    if not selection['nodes']:
        raise dash.exceptions.PreventUpdate

    selected_node_id = selection['nodes'][0]
    selected_node = next(node for node in net_data['nodes'] if node['id'] == selected_node_id)

    selected_node_info = f"選択されたノード: {selected_node['label']}"

    selected_net_data = {
        'nodes': [selected_node],
        'edges': [edge for edge in net_data['edges'] if edge['from'] == selected_node_id or edge['to'] == selected_node_id]
    }
    print(selected_net_data)
    return net_data, selected_node_info, selected_node['label'], selected_net_data

@app.callback(
    Output('net', 'data', allow_duplicate=True),
    Output('selected-net', 'data', allow_duplicate=True),
    Output('loading-output', 'children'),
    Input('add-button', 'n_clicks'),
    Input('generate-graph-button', 'n_clicks'),
    Input('similarity-button', 'n_clicks'),
    State('textarea-input', 'value'),
    State('net', 'selection'),
    State('net', 'data'),
    State('selected-net', 'data'),
    prevent_initial_call=True
)
def handle_buttons(add_clicks, generate_clicks, similarity_clicks, input_text, selection, net_data, selected_net_data):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    loading_message = ''
    if button_id == 'add-button':
        if not input_text:
            raise dash.exceptions.PreventUpdate
        
        # ロード画面を表示
        loading_message = '追加中...'
        new_map = reflection_map(input_text)
        
        # ノードを更新
        new_nodes = {node['id']: node for node in new_map['nodes']}
        for i, node in enumerate(net_data['nodes']):
            if node['id'] in new_nodes:
                net_data['nodes'][i] = new_nodes.pop(node['id'])
        net_data['nodes'].extend(new_nodes.values())
        
        # エッジを更新
        new_edges = {(edge['from'], edge['to']): edge for edge in new_map['edges']}
        for i, edge in enumerate(net_data['edges']):
            edge_tuple = (edge['from'], edge['to'])
            if edge_tuple in new_edges:
                net_data['edges'][i] = new_edges.pop(edge_tuple)
        net_data['edges'].extend(new_edges.values())
        
        loading_message = ''

    elif button_id == 'generate-graph-button':
        # ロード画面を表示
        loading_message = 'グラフ生成中...'
        
        selected_nodes = [node for node in net_data['nodes'] if node['id'] in selection['nodes']]
        selected_edges = [edge for edge in net_data['edges'] if edge['from'] in selection['nodes'] or edge['to'] in selection['nodes']]
        
        modified_data = relate_map(selected_nodes, selected_edges)
        
        loading_message = ''
        
        return net_data, modified_data, loading_message
    
    elif button_id == 'similarity-button':
        # ロード画面を表示
        loading_message = '類似度計算中...'
        
        if len(selected_net_data['nodes']) < 2:
            raise dash.exceptions.PreventUpdate
        
        map1 = {'nodes': [selected_net_data['nodes'][0]], 'edges': []}
        map2 = {'nodes': [selected_net_data['nodes'][1]], 'edges': []}
        
        new_map = similar_add_edge(map1, map2)
        
        net_data['nodes'].extend(new_map['nodes'])
        net_data['edges'].extend(new_map['edges'])
        
        loading_message = ''

    return net_data, dash.no_update, loading_message

@app.callback(
    Output('net', 'data', allow_duplicate=True),
    Input('dropdown-selection_map', 'value'),
    State('net', 'data'),
    prevent_initial_call=True  # ここを追加します
)
def update_map(selected_map,net_data):
    net_data['nodes'] = [node for node in net_data['nodes'] if '振り返り' in node['id']]
    net_data['edges'] = [edge for edge in net_data['edges'] if '振り返り' in edge['from'] or '振り返り' in edge['to']]
    if selected_map==3:
    # IDに「振り返り」が含まれるノードとエッジをフィルタリング
        return net_data
    else:
        tmp_nodes, tmp_edges = load_csv_data(dropdown_list[selected_map])
        #initial_nodes.extend(tmp_nodes)
        #initial_edges.extend(tmp_edges)
        net_data['nodes'].extend(tmp_nodes)
        net_data['edges'].extend(tmp_edges)
        return net_data

@app.callback(
    Output('net', 'data', allow_duplicate=True),
    Input('reflect-changes-button', 'n_clicks'),
    State('selected-net', 'data'),
    State('net', 'data'),
    prevent_initial_call=True
)
def reflect_changes(n_clicks, selected_net_data, net_data):
    updated_nodes = net_data['nodes'] + [node for node in selected_net_data['nodes'] if node not in net_data['nodes']]
    updated_edges = net_data['edges'] + [edge for edge in selected_net_data['edges'] if edge not in net_data['edges']]
    
    return {'nodes': updated_nodes, 'edges': updated_edges}

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000, debug=True)
