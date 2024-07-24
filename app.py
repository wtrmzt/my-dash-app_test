import dash
from dash import dcc, html, Input, Output
import visdcc
import pandas as pd
import networkx as nx#

app = dash.Dash(__name__)
num = 0

# ドロップダウンのオプション
centrality_options = [
    {'label': '次数中心性', 'value': 'degree_centrality'},
    {'label': '固有ベクトル中心性', 'value': 'eigenvector_centrality'},
    {'label': 'ページランク', 'value': 'pagerank'},
    {'label': '媒介中心性', 'value': 'betweenness_centrality'},
    {'label': '情報中心性', 'value': 'information_centrality'}
]

# 
nodes=[
{'id': 'コンピューターリテラシー_0', 'label': 'コンピュータリテラシー', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_1', 'label': 'コンピュータの基本構成', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_2', 'label': 'テキスト整形・記述', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_3', 'label': '情報セキュリティ', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_4', 'label': 'コンピュータの利用と認証', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_5', 'label': 'インターネットの原理', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_6', 'label': 'ネットワークと安全性', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_7', 'label': 'コンピュータの動作原理', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_8', 'label': 'ファイルシステムとファイル操作', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_9', 'label': 'テキストファイルとエディタ', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_10', 'label': 'コンピュータシステムとOS', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_11', 'label': 'フィルタとシェルスクリプト', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_12', 'label': 'マークアップによるテキスト整形', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_13', 'label': 'グラフィックス/図と表', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_14', 'label': 'アカデミックリテラシ', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_15', 'label': 'Webページ記述と情報アーキテクチャ', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_16', 'label': 'ソフトウェア開発とテストケース', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_17', 'label': '認証', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_18', 'label': 'パスワード', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_19', 'label': 'Unix', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_20', 'label': 'TCP/IP', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_21', 'label': 'IPアドレス', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_22', 'label': 'DNS', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_23', 'label': '情報セキュリティ', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_24', 'label': '暗号技術', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_25', 'label': 'PKI', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_26', 'label': 'SSH', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_27', 'label': 'World Wide Web', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_28', 'label': '電子メール', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_29', 'label': 'プログラム', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_30', 'label': '小さなコンピュータ', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_31', 'label': 'ファイルシステム', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_32', 'label': 'ディレクトリの操作', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_33', 'label': 'ファイルの保護設定', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_34', 'label': '文字コード/UNICODE,UTF8', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_35', 'label': 'Emacsの操作', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_36', 'label': 'マルチタスク', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_37', 'label': 'プロセス観察', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_38', 'label': 'リダイレクションとパイプ', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_39', 'label': 'ユティリティ', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_40', 'label': 'フィルタ', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_41', 'label': '置換', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_42', 'label': '整列', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_43', 'label': '正規表現', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_44', 'label': 'マークアップ方式', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_45', 'label': 'LaTeX', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_46', 'label': 'ピクセルグラフィックス', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_47', 'label': 'ベクターグラフィックス', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_48', 'label': 'LaTeXに画像を挿入', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_49', 'label': 'PostScript', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_50', 'label': 'HTML', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_51', 'label': 'CSS', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_52', 'label': 'ブロック要素', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_53', 'label': 'インライン要素', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_54', 'label': '絶対URL', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_55', 'label': '相対URL', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_56', 'label': 'サイト構造', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_57', 'label': 'パディング', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_58', 'label': 'CSSグリッド', 'color': '#F8C6BD'},

{'id': 'コンピューターリテラシー_59', 'label': 'JavaScript', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_60', 'label': '高水準言語', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_61', 'label': '低水準言語', 'color': '#F8C6BD'},
{'id': 'コンピューターリテラシー_62', 'label': 'テスト', 'color': '#F8C6BD'}
                  ]

edges=[
{'from': 'コンピューターリテラシー_0','to': 'コンピューターリテラシー_1'},
{'from': 'コンピューターリテラシー_0','to': 'コンピューターリテラシー_2'},
{'from': 'コンピューターリテラシー_0','to': 'コンピューターリテラシー_3'},
{'from': 'コンピューターリテラシー_1','to': 'コンピューターリテラシー_5'},
{'from': 'コンピューターリテラシー_1','to': 'コンピューターリテラシー_7'},
{'from': 'コンピューターリテラシー_1','to': 'コンピューターリテラシー_8'},
{'from': 'コンピューターリテラシー_1','to': 'コンピューターリテラシー_10'},
{'from': 'コンピューターリテラシー_1','to': 'コンピューターリテラシー_11'},
{'from': 'コンピューターリテラシー_1','to': 'コンピューターリテラシー_13'},
{'from': 'コンピューターリテラシー_2','to': 'コンピューターリテラシー_9'},
{'from': 'コンピューターリテラシー_2','to': 'コンピューターリテラシー_12'},
{'from': 'コンピューターリテラシー_2','to': 'コンピューターリテラシー_14'},
{'from': 'コンピューターリテラシー_2','to': 'コンピューターリテラシー_15'},
{'from': 'コンピューターリテラシー_3','to': 'コンピューターリテラシー_4'},
{'from': 'コンピューターリテラシー_3','to': 'コンピューターリテラシー_6'},
{'from': 'コンピューターリテラシー_3','to': 'コンピューターリテラシー_16'},
{'from': 'コンピューターリテラシー_4','to': 'コンピューターリテラシー_17'},
{'from': 'コンピューターリテラシー_4','to': 'コンピューターリテラシー_18'},
{'from': 'コンピューターリテラシー_5','to': 'コンピューターリテラシー_19'},
{'from': 'コンピューターリテラシー_5','to': 'コンピューターリテラシー_20'},
{'from': 'コンピューターリテラシー_5','to': 'コンピューターリテラシー_21'},
{'from': 'コンピューターリテラシー_5','to': 'コンピューターリテラシー_22'},
{'from': 'コンピューターリテラシー_6','to': 'コンピューターリテラシー_23'},
{'from': 'コンピューターリテラシー_6','to': 'コンピューターリテラシー_24'},
{'from': 'コンピューターリテラシー_6','to': 'コンピューターリテラシー_25'},
{'from': 'コンピューターリテラシー_6','to': 'コンピューターリテラシー_26'},
{'from': 'コンピューターリテラシー_6','to': 'コンピューターリテラシー_27'},
{'from': 'コンピューターリテラシー_6','to': 'コンピューターリテラシー_28'},
{'from': 'コンピューターリテラシー_7','to': 'コンピューターリテラシー_29'},
{'from': 'コンピューターリテラシー_7','to': 'コンピューターリテラシー_30'},
{'from': 'コンピューターリテラシー_8','to': 'コンピューターリテラシー_31'},
{'from': 'コンピューターリテラシー_8','to': 'コンピューターリテラシー_32'},
{'from': 'コンピューターリテラシー_8','to': 'コンピューターリテラシー_33'},
{'from': 'コンピューターリテラシー_9','to': 'コンピューターリテラシー_34'},
{'from': 'コンピューターリテラシー_9','to': 'コンピューターリテラシー_35'},
{'from': 'コンピューターリテラシー_10','to': 'コンピューターリテラシー_36'},
{'from': 'コンピューターリテラシー_10','to': 'コンピューターリテラシー_37'},
{'from': 'コンピューターリテラシー_10','to': 'コンピューターリテラシー_38'},
{'from': 'コンピューターリテラシー_11','to': 'コンピューターリテラシー_39'},
{'from': 'コンピューターリテラシー_11','to': 'コンピューターリテラシー_40'},
{'from': 'コンピューターリテラシー_11','to': 'コンピューターリテラシー_41'},
{'from': 'コンピューターリテラシー_11','to': 'コンピューターリテラシー_42'},
{'from': 'コンピューターリテラシー_11','to': 'コンピューターリテラシー_43'},
{'from': 'コンピューターリテラシー_12','to': 'コンピューターリテラシー_44'},
{'from': 'コンピューターリテラシー_12','to': 'コンピューターリテラシー_45'},
{'from': 'コンピューターリテラシー_13','to': 'コンピューターリテラシー_46'},
{'from': 'コンピューターリテラシー_13','to': 'コンピューターリテラシー_47'},
{'from': 'コンピューターリテラシー_13','to': 'コンピューターリテラシー_48'},
{'from': 'コンピューターリテラシー_13','to': 'コンピューターリテラシー_49'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_50'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_51'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_52'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_53'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_54'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_55'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_56'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_57'},
{'from': 'コンピューターリテラシー_15','to': 'コンピューターリテラシー_58'},
{'from': 'コンピューターリテラシー_16','to': 'コンピューターリテラシー_59'},
{'from': 'コンピューターリテラシー_16','to': 'コンピューターリテラシー_60'},
{'from': 'コンピューターリテラシー_16','to': 'コンピューターリテラシー_61'},
{'from': 'コンピューターリテラシー_16','to': 'コンピューターリテラシー_62'}
]





# ノードとエッジをvisdccのデータ形式に変換
nodes_for_visdcc = [{'id': node['id'], 'label': node['label'], 'color': node['color']} for node in nodes]
edges_for_visdcc = [{'from': edge['from'], 'to': edge['to']} for edge in edges]

app.layout = html.Div([
    html.Div(style={'width': '5%', 'height': '100vh', 'backgroundColor': '#4285f4', 'float': 'left'}),
    html.Div([
        dcc.Dropdown(
            id='centrality-dropdown',
            options=centrality_options,
            value='degree_centrality',
            style={'margin': '20px'}
        ),
        visdcc.Network(
            id='net',
            data={'nodes': nodes_for_visdcc, 'edges': edges_for_visdcc},
            options={
                'height': '900px', 'width': '100%',
                'clickToUse': True,
                'physics': {'barnesHut': {'avoidOverlap': 0}},
                'layout': {'randomSeed': num}
            }
        )
    ], style={'width': '95%', 'float': 'left'})
])

@app.callback(
    Output('net', 'data'),
    [Input('centrality-dropdown', 'value')]
)



def update_graph(centrality_type):
    # 中心性に応じてグラフのデータを更新するロジックをここに追加
    # 例えば、ノードの色を変えたり、サイズを変更するなど
    map_data={'nodes':nodes,'edges':edges}
    #print(centrality_type)
    G = nx.Graph()

    # ノードの追加
    for node in map_data['nodes']:
        G.add_node(node['id'], label=node['label'])

    # エッジの追加
    for edge in map_data['edges']:
        G.add_edge(edge['from'], edge['to'])

    centrality = pd.Series(nx.degree_centrality(G),name="degree_centrality")

    if(centrality_type == "degree_centrality"):
        # 次数中心性の計算
        centrality = pd.Series(nx.degree_centrality(G),name="degree_centrality")
    elif(centrality_type == "eigenvector_centrality"):
        # 固有ベクトル中心性の計算
        centrality = pd.Series(nx.eigenvector_centrality_numpy(G),name="eigenvector_centrality")
    elif(centrality_type == "pagerank"):
        # ページランク：PageRank
        centrality = pd.Series(nx.pagerank(G), name="pagerank")
    elif(centrality_type =="betweenness_centrality"):
        # 媒介中心性：Betweeness centrality
        centrality = pd.Series(nx.betweenness_centrality(G), name="betweenness_centrality")
    elif(centrality_type == "information_centrality"):
        # 情報中心性：Information centrality
        centrality = pd.Series(nx.information_centrality(G), name="information_centrality")

    gg_centrality_rank = pd.concat([
    centrality
    ], axis=1).rank(ascending=False)

    # 正規化
    nomalized_gg_centrality_rank = gg_centrality_rank

    #print(nomalized_gg_centrality_rank)

    #print(nomalized_gg_centrality_rank)
    comoku = centrality_type
    # ノードの色を中心性に基づいて設定
    nomalized_gg_centrality_rank[comoku] = (gg_centrality_rank[comoku] - gg_centrality_rank[comoku].min()) / (gg_centrality_rank[comoku].max() - gg_centrality_rank[comoku].min())
    for node in map_data['nodes']:
        #print(node['id'])
        tmp = 255 - int(255 * nomalized_gg_centrality_rank[comoku][node['id']])
        rgb_code = (tmp, tmp, tmp)

        hex_code = "#{:02x}{:02x}{:02x}".format(*rgb_code)
        node['color'] = hex_code
    return {'nodes': nodes, 'edges': edges}
    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000, debug=True)
