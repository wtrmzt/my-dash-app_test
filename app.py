# ファイル名: app.py (または visualize_graph.py など)

import csv
import dash
from dash import html # dcc は現時点では未使用
import visdcc
import logging
import os
# from flask import Flask # Dash内で使用されるため、明示的なインポートは通常不要

# --- ロギング設定 (Render環境向けに調整) ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    # Renderは標準出力/エラーのログを収集するためStreamHandlerを使用
                    handlers=[logging.StreamHandler()])

# --- ノードデータ ---
# (ご提供いただいた all_nodes リスト全体をここに記述してください)
all_nodes = [
    { "id":"アルゴリズム論第一","label":"アルゴリズム，正当性，停止性，計算量，データ構造，線形構造，木構造，ハッシュ法，ヒープ，探索木，平衡探索木，グラフ"},
    { "id":"アルゴリズム論第二","label":"アルゴリズム，計算量，グラフ，最短路，動的計画法，文字列照合，文法，隠れマルコフモデル，NP完全，NP困難，分枝限定法，近似アルゴリズム"},
    { "id":"インタラクティブシステム","label":"フーリエ変換、相互相関、自己相関、ラプラス変換、行列、センシング、信号処理、画像処理、制御、ロボティクス"},
    { "id":"オペレーションズ・リサーチ基礎","label":"数理モデル、最適化、線形計画法、動的計画法、ゲーム理論、待ち行列、プロジェクトスケジューリング"},
    { "id":"オペレーションズ・リサーチ第一","label":"意思決定; 効用関数; 経済発注量; 新聞売り子; 発注点; 在庫管理; 割当問題; 輸送問題; 双対単体法; 非線形最適化; ラグランジュの未定定数法; KKT条件; 待ち行列理論; 確率過程"},
    { "id":"オペレーションズ・リサーチ第二","label":"離散最適化"},
    { "id":"グラフとネットワーク","label":"グラフ、ネットワーク、道、閉路、木、平面グラフ、彩色、辺彩色、マッチング、最大流"},
    { "id":"ゲーム情報学","label":"ボードゲーム、パズル、ヒューリスティック探索、評価関数Board game, Puzzle, Heuristic Search, Evaluation Function"},
    { "id":"コミュニケーション論","label":"コミュニケーション，認知，身体，進化，人間，科学技術，情報技術，社会，スポーツ"},
    { "id":"コンピュータグラフィックス","label":"OpenGL、三次元座標変換、テクスチャマッピング、ラジオシティ法、CUDA"},
    { "id":"コンピュータネットワーク","label":"ネットワークアーキテクチャ、プロトコル、通信システム、OSI、TCP/IP、LAN、WAN"},
    { "id":"コンピュータリテラシー","label":"計算機の基本構成、 ログイン、 ログアウト、 UNIX、 コマンド、 ファイル、 文書編集、 エディタ、 コンピュータネットワーク、 電子メール、Web、 WWW、 HTML、 セキュリティ、 情報の検索、情報倫理、文書整形、LaTeX"},
    { "id":"コンピュータ設計論","label":"コンピュータの構成と設計，プロセッサ，キャッシュ，並列プロセッサ，高速化"},
    { "id":"サイエンス・コミュニケーション演習（集中）","label":"サイエンス　コミュニケーション"},
    { "id":"シミュレーション理工学","label":"シミュレーション、物理モデル、数理モデル、数値解析、微分方程式"},
    { "id":"ソフトウェア工学","label":"ソフトウェア開発，オブジェクト指向，ＵＭＬ，デザインパターン"},
    { "id":"データサイエンス","label":"回帰分析、ベイズ統計、機械学習、最小二乗法、マルコフ連鎖モンテカルロ法"},
    { "id":"データサイエンス演習","label":"データサイエンス、人工知能、機械学習Data science, Artificial Intelligence, Machine learning"},
    { "id":"データベース論","label":"リレーショナルデータベース，リレーショナル代数，正規化，SQL，質問処理，データベース管理システム(DBMS)，トランザクション，データサイエンス"},
    { "id":"ハイパフォーマンスコンピューティング","label":"高性能計算、連立1次方程式、ガウス消去法、LU分解、反復法、共役勾配法、固有値問題、高速フーリエ変換"},
    { "id":"ヒューマンインタフェース","label":"対話システムのデザイン，キーボードと日本語入力，ポインティングデバイス，ペン，モバイルデバイス，音声認識，画像認識，視覚出力，可視化，音声合成，触覚出力，ヒューマンコンピュータインタラクション，マルチモーダル音声対話システムの現状"},
    { "id":"ビジュアル情報処理","label":"コンピュータグラフィックス，画像処理，座標変換，形状表現，レンダリング，アニメーション"},
    { "id":"プログラミング言語実験","label":"計算機言語、イベント駆動型言語、関数型言語、オブジェクト指向"},
    { "id":"プログラミング通論","label":"ブロック構造, 引数機構, 再帰呼出し, スタック, キュー, デク, ポインタ, リスト, 整列, マージ, 探索"},
    { "id":"プログラム言語論","label":"C，C++，Java，Lisp，Prolog"},
    { "id":"ベンチャービジネス概論","label":"エクイティファイナンス、イノベーション、革新性、成長率、EXIT（出口戦略）、資本調達法、プロダクトマーケットフィット、IP・知的財産資産ビジネス、研究成果型ベンチャー"},
    { "id":"マルチメディア処理（Ⅰ類）","label":"物理量、感覚量、情報のディジタル化、符号化、ファイル形式、音声処理、画像処理、データ量、3次元コンピュータグラフィックス、情報の可視化、オーサリング、マルチメディアシステム"},
    { "id":"マーケティング科学","label":"機械学習; 情報推薦; 時系列予測; 因果推論; テキストマイニング"},
    { "id":"メディアリテラシー","label":"メディア、映像、コンテンツデザイン、デジタル・ディバイディング、広告"},
    { "id":"メディア分析法","label":"感性、五感、言語、オノマトペ、分析法、人工知能"},
    { "id":"メディア情報学プログラミング演習","label":"オブジェクト指向プログラミング，Java言語，GUIプログラミング，グループプログラミング，OpenJDK, Swing"},
    { "id":"メディア情報学実験","label":"メディア制作，メディア分析，認識"},
    { "id":"メディア論","label":"メディアデザイン、メディア理論、インタラクションデザイン、 ユーザーインターフェース、メディアアート、ミュージアム"},
    { "id":"メンタルヘルス論","label":"精神医学、心理学、メンタルヘルス、自殺予防、うつ病、発達障害、脳科学"},
    { "id":"ユビキタスネットワーク","label":"知的・自律的エージェント，ロボット，インタラクティブシステム，プライバシー，知的活動支援，支援ジレンマ，超人スポーツ，ソフトウェア開発手法，インテリジェントシステム，バーチャルリアリティ，認知モデル，人間拡張技術，触力覚提示"},
    { "id":"信頼性工学","label":"品質保証、信頼性設計、信頼性データ解析、システムの信頼性、安全性設計"},
    { "id":"倫理学と哲学の間","label":"『永遠平和のために』、カント、平和論、社会契約論"},
    { "id":"化学概論第一","label":"プランク定数・ラザフォードモデル・リュードベリ定数・ボーアの振動数条件・量子条件・ボーア半径・量子数・パウリの排他律・フント則・ドブロイ波・不確定性原理・波動方程式・周期律・構成原理・遮蔽効果・特性X線・モーズリーの法則・イオン化エネルギー・電子親和力・共有電子対・分子軌道法・LCAO-MO・結合性軌道・反結合性軌道・π軌道・混成軌道・非共有電子対・電気陰性度・極性分子・双極子モーメント・配位結合・水素結合・金属結合・自由電子・半導体"},
    { "id":"化学概論第二","label":"熱力学第一法則, エンタルピー，熱容量, 反応熱, エントロピー，熱力学第二法則, 自由エネルギー，化学平衡, 電気化学, 電気エネルギー, 核エネルギー"},
    { "id":"品質管理第一","label":"品質管理、SQC、TQM"},
    { "id":"品質管理第二","label":"品質管理、品質機能展開、実験計画法、タグチメソッド、システム工学"},
    { "id":"基礎プログラミングおよび演習","label":"プログラム、データ型、構造体、式、制御構造、関数、アルゴリズム、構造化プログラミング、デバッグ"},
    { "id":"多変量解析","label":"Statistical learning, Machine learning, Data mining, Python.統計的学習理論, 機械学習, データマイニング, Python."},
    { "id":"宇宙・地球科学","label":"宇宙、天文学、銀河、恒星、惑星、ブラックホール"},
    { "id":"幾何学概論（Ⅰ類）","label":"平面曲線，空間曲線，曲率，曲率半径，捩率，回転数"},
    { "id":"形式言語理論","label":"- Formal language（形式言語）- Finite automaton（有限オートマトン）- Regular expression（正則表現）- Regular language（正則言語）- Non-determinism（非決定性）- Minimization of finite automata（有限オートマトンの最小化）- Grammar（文法）- Chomsky hierarchy（チョムスキー階層）"},
    { "id":"微分積分学第一","label":"◆実数の連続性，上限，下限，逆三角関数　◆合成関数の微分，逆関数の微分，対数微分法，平均値の定理，ロピタルの定理，連続微分可能，ライプニッツの公式，テーラーの定理，マクローリン展開　◆定積分，不定積分，部分積分，置換積分，広義積分，区分求積法"},
    { "id":"微分積分学第二","label":"◆偏微分，偏導関数，全微分，ヤコビアン，接平面，法線，テーラーの定理，極値問題，偏微分作用素，ラプラシアン，陰関数，条件付き極値，ラグランジュの未定乗数法　◆重積分，累次積分，変数変換，極座標，線積分，グリーンの定理，曲面積"},
    { "id":"応用代数学","label":"群・リー群・リー環・回転群"},
    { "id":"応用数学第一","label":"--フーリエ級数--周期関数，相互相関関数，自己相関関数，周期的畳み込み，フーリエ係数，フーリエ級数，複素フーリエ係数，複素フーリエ級数，関数の区分的連続性，関数の区分的なめらか性，ディリクレの収束定理，ギブス現象，畳み込み定理，相互相関定理，自己相関定理，パーセヴァルの等式--フーリエ変換-- 絶対可積分関数，2乗可積分関数，非周期関数，相互相関関数，自己相関関数，畳み込み，フーリエ変換，逆フーリエ変換，フーリエ積分定理，畳み込み定理，相互相関定理，自己相関定理，パーセヴァルの等式，テスト関数，汎関数，シュワルツ超関数，デルタ関数，周期的デルタ関数，弱微分，超関数微分，微分方程式の解法"},
    { "id":"応用数学第二","label":"ベクトル場，勾配，回転，発散，線積分，面積分，ガウスの定理，ストークスの定理，直交曲線座標，ラプラス方程式，熱伝導方程式，波動方程式，基本解，最大値原理Vector field, gradient, rotation, divergence, line integral, surface integral, Gauss’s theorem, Stokes’s theorem, orthogonal curvilinear coordinates, Laplace equation, heat equation, wave equation, fundamental solution, maximum principle"},
    { "id":"情報通信システム","label":"情報理論、符号理論、符号化、情報量、エントロピー"},
    { "id":"情報領域演習第一","label":"離散数学，プログラミング"},
    { "id":"情報領域演習第三","label":"再帰的手続き，スタック，キュー，線形リスト，木構造，ハッシング，ヒープ，探索木，平衡探索木，グラフ構造"},
    { "id":"情報領域演習第二","label":"プログラミング，論理設計学，計算機通論，確率論"},
    { "id":"技術者倫理","label":"技術者、職業倫理、公益、プロフェッショナル、説明責任"},
    { "id":"数値解析","label":"数値計算、数値解析、誤差評価"},
    { "id":"数値計算","label":"計算科学、シミュレーション科学、データ科学"},
    { "id":"数学演習第一","label":"微分積分学第一，線形代数学第一を参照"},
    { "id":"数学演習第二","label":"微分積分学第二，線形代数学第二を参照"},
    { "id":"数理計画法","label":"オペレーションズ・リサーチ, 数理最適化問題，線形計画問題， 双対性，最適性条件，アルゴリズム，プログラミング."},
    { "id":"材料化学","label":"化学、機能性物質、遷移金属、d電子、有機材料、π電子、セラミックス、半導体、超伝導、磁性、高分子材料、エネルギー変換、光の吸収と色"},
    { "id":"物体認識論","label":"画像認識，物体認識，特徴抽出，機械学習，深層学習，MATLAB"},
    { "id":"物理学概論第一","label":"物理学，力学，波"},
    { "id":"物理学概論第三","label":"量子論、粒子性と波動性、原子核、現代社会"},
    { "id":"物理学概論第二","label":"物理学，熱，電磁気学"},
    { "id":"物理学演習第一","label":"物理学、力学、波動"},
    { "id":"物理学演習第二","label":"物理学、熱学、電磁気学"},
    { "id":"現代数学入門Ａ","label":"命題，集合，写像，濃度，実数の連続性，Cauchy列，近傍，開集合・閉集合，Euclid空間，コンパクト集合，距離空間，Banach空間，一様収束"},
    { "id":"現代数学入門Ｂ","label":"群，環，体，群の作用，"},
    { "id":"環境論","label":"土壌生態系，都市の緑化，森林衰退，大気汚染ガス，野生生物，環境変動，森林利用，地球温暖化，自然浄化機能，森林消失，水保全"},
    { "id":"生産管理","label":"生産管理、在庫管理、生産システム、需要予測、生産計画、日程計画、サプライチェーン、経営情報システム、環境経営、ヘルスケアシステム工学"},
    { "id":"知的情報処理","label":"人工知能、探索、データマイニング、パターン認識と機械学習"},
    { "id":"知的財産権","label":"知的財産・特許・発明・著作物・著作権・不正競争・意匠・商標・実用新案・考案"},
    { "id":"確率論","label":"確率，確率変数，確率分布，モーメント，大数の法則，中心極限定理，分布論"},
    { "id":"社会情報論","label":"高度情報通信ネットワーク社会，共創進化スマート社会，Society 5.0，ICT，時空間情報，公共選択"},
    { "id":"経営・社会情報学実験","label":"学生実験"},
    { "id":"統計学","label":"推定論，検定論，尤度"},
    { "id":"線形代数学第一","label":"◆行列とその演算 ◆正則行列　◆行基本変形，簡約行列 ◆連立１次方程式 ◆逆行列 ◆行列の階数　◆行列式　◆余因子展開，余因子行列"},
    { "id":"線形代数学第二","label":"◆ベクトル空間　◆１次独立・１次従属　◆部分空間　◆和空間　◆ベクトル空間の基底と次元 ◆座標 ◆線形写像　◆線形写像の表現行列　◆線形写像の核と像 ◆基底変換行列　◆固有値，固有ベクトル◆対角化"},
    { "id":"複素関数論（Ⅰ類）","label":"複素数、複素平面、オイラーの公式、初等関数、正則関数、コーシー・リーマンの関係式、調和関数、コーシーの積分定理、テイラー展開、ローラン展開、特異点、極、留数定理"},
    { "id":"解析学","label":"◆級数，正項級数，等比級数，コーシーの判定法，ダランベールの判定法，絶対収束，整級数，収束半径，テーラー展開　◆微分方程式，正規形，変数分離形，同次形，１階線形微分方程式，完全微分形，積分因子，特殊解，一般解，斉次方程式，特性方程式"},
    { "id":"言語処理系論","label":"コンパイラ，インタプリタ，抽象機械，部分評価，コンパイラ最適化"},
    { "id":"言語認知工学","label":"自然言語処理、言語認知科学、意味表現、ニューラルネットワーク、意味空間モデル、言語モデル、ネットワーク科学、情報検索"},
    { "id":"計算機通論_1","label":"コンピュータアーキテクチャ、アセンブリ言語、ノイマン型計算機、数の表現"},
    { "id":"計算理論","label":"計算可能性、計算量、ＮＰ完全性、チューリング機械"},
    { "id":"認知科学","label":"認知科学，認知心理学，認知，心理学，脳，身体，進化，言語，学習，記憶，知覚，感覚，思考，障害，人工知能"},
    { "id":"論理設計学","label":"ディジタル回路、組合せ論理回路、順序回路、フリップフロップ、カウンタ、シフトレジスタ、ブール代数"},
    { "id":"進化計算論","label":"人工知能，進化計算，複雑系，創発，シミュレーション"},
    { "id":"運動と筋の科学","label":"運動生理学，生物学，運動トレーニング"},
    { "id":"金融工学（集中）","label":"リスク管理、ポートフォリオ理論、デリバティブ理論、ブラックショールズモデル"},
    { "id":"離散数学","label":"集合、写像、命題論理、述語論理、２項関係、数学的帰納法、グラフ理論、濃度"},
    { "id":"離散数理工学","label":"組合せ論，数え上げ，漸化式，母関数，二項係数，カタラン数，スターリング数，分割，ベル数，確率，期待値，マルコフの不等式，チェルノフ限界，マルコフ連鎖，推移確率，定常分布，ランダムウォーク，乱択アルゴリズム"},
    { "id":"電気・電子回路","label":"直流回路、交流回路、周波数特性、微分回路、積分回路、トランジスター、オペアンプ"},
    { "id":"音響信号処理","label":"音，音響，オーディオ，応用数学"}
]
logging.info(f"定義されたノード数: {len(all_nodes)}")

# --- 定数 ---
EDGES_FILENAME = "related_edges.csv" # エッジ情報CSVファイル

# --- エッジデータの読み込み ---
edges_for_vis = []
node_ids_set = {node['id'] for node in all_nodes} # 高速な存在確認のためセットを使用

# Renderのファイルシステムは一時的ですが、デプロイ時に含めれば読み込みは可能です
csv_file_path = os.path.join(os.path.dirname(__file__), EDGES_FILENAME) # スクリプトと同じディレクトリを想定

if os.path.exists(csv_file_path):
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                try:
                    source_id = row['Source']
                    target_id = row['Target']
                    score = float(row['Score'])

                    if source_id in node_ids_set and target_id in node_ids_set:
                        edges_for_vis.append({
                            'from': source_id,
                            'to': target_id,
                            'value': score,
                            'title': f"Score: {score:.4f}",
                            'width': max(0.5, 1.0 + score * 4.0),
                            'color': {'color': '#848484', 'highlight': '#2B7CE9', 'hover': '#2B7CE9'}
                        })
                    else:
                        logging.warning(f"CSV {i+1}行目: エッジ ({source_id} <=> {target_id}) のノードが定義されたノードリストに含まれていません。無視します。")

                except KeyError as e:
                    logging.error(f"CSVファイル '{EDGES_FILENAME}' の {i+1}行目に必要な列が見つかりません: {e}。ヘッダーを確認してください。")
                    continue
                except ValueError:
                    logging.warning(f"CSVファイル '{EDGES_FILENAME}' の {i+1}行目: 'Score'列の値 '{row.get('Score', '')}' を数値に変換できませんでした。無視します。")
                    continue
                except Exception as e:
                    logging.error(f"CSVファイル '{EDGES_FILENAME}' の {i+1}行目の処理中に予期せぬエラーが発生しました: {e}")
                    continue

        logging.info(f"'{EDGES_FILENAME}' から {len(edges_for_vis)} 件の有効なエッジ情報を読み込みました。")

    except FileNotFoundError:
        # ファイルが見つからない場合、エラーログを出力し、空のエッジリストで続行
        logging.error(f"エッジファイル '{csv_file_path}' が見つかりません。アプリは起動しますが、エッジは表示されません。")
    except Exception as e:
        logging.error(f"'{EDGES_FILENAME}' の読み込み処理中にエラーが発生しました: {e}")
else:
    logging.warning(f"エッジファイル '{csv_file_path}' が見つかりません。エッジなしでグラフを表示します。")


# --- 可視化用ノードデータの準備 ---
nodes_for_vis = []
for node in all_nodes:
    nodes_for_vis.append({
        'id': node['id'],
        'label': node['id'], # グラフ上のラベルはID (ご提示のコード通り)
        'title': node['label'], # マウスオーバー時のタイトルは元の長いラベル
        'shape': 'ellipse',
        # 'font': {'size': 14} # オプションでフォントサイズ指定可能 (vis_optionsでも設定可)
    })

# --- Dash アプリケーションのインスタンス化 ---
# requests_pathname_prefix は通常Renderでは不要ですが、
# サブディレクトリでホストする場合などは設定が必要になることがあります。
app = dash.Dash(__name__)
app.title = "ノード関連性グラフ"

# --- ★ WSGIサーバー (gunicorn) が参照するサーバーオブジェクト ---
# Dashアプリケーション(`app`)が持つFlaskサーバーインスタンスを `server` 変数に代入
server = app.server

# --- visdcc.Network の表示オプション設定 ---
# (vis_options 辞書の内容は変更ありません - ご提示のものをそのまま使用)
vis_options = {
    'height': '800px', 'width': '100%',
    'physics': {
        'enabled': True, 'solver': 'forceAtlas2Based',
        'forceAtlas2Based': {
            'gravitationalConstant': -40, 'centralGravity': 0.01,
            'springLength': 100, 'springConstant': 0.05,
            'damping': 0.09, 'avoidOverlap': 0.1
        },
        'stabilization': {
             'enabled': True, 'iterations': 1000, 'updateInterval': 50,
             'onlyDynamicEdges': False, 'fit': True
         }
    },
    'interaction': {
        'tooltipDelay': 200, 'hideEdgesOnDrag': False, 'hideNodesOnDrag': False,
        'navigationButtons': True, 'keyboard': True, 'hover': True
     },
    'nodes': {
        'borderWidth': 1, 'borderWidthSelected': 2, 'shape': 'ellipse', 'size': 20,
        'color': {
            'border': '#2B7CE9', 'background': '#D2E5FF',
            'highlight': {'border': '#2B7CE9', 'background': '#FBFCFF'},
            'hover': {'border': '#2B7CE9', 'background': '#9ECEFF'}
        },
        'font': {
            'color': '#343434', 'size': 12, 'face': 'arial',
            'strokeWidth': 0, 'strokeColor': '#ffffff'
        }
    },
    'edges': {
        'width': 1,
        'color': {
            'color': '#848484', 'highlight': '#848484', 'hover': '#2B7CE9',
            'inherit': False, 'opacity': 0.7
        },
        'arrows': {'to': {'enabled': False}, 'middle': {'enabled': False}, 'from': {'enabled': False}},
        'smooth': {'enabled': True, 'type': "continuous", 'roundness': 0.5}
    }
}

# --- Dash アプリケーションのレイアウト定義 ---
app.layout = html.Div(children=[
    html.H1(children="ノード関連性 可視化", style={'textAlign': 'center', 'marginBottom': '20px'}),
    visdcc.Network(
        id='net',
        data={'nodes': nodes_for_vis, 'edges': edges_for_vis},
        options=vis_options
    ),
    html.P(
        # ファイルパスではなくファイル名を表示する方が一般的
        f"（ノード数: {len(nodes_for_vis)}, エッジ数: {len(edges_for_vis)} - '{os.path.basename(csv_file_path)}' から読み込み）",
        style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': 'small', 'color': 'gray'}
    )
])

# --- サーバー起動部分 (Renderでは不要) ---
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000, debug=True)
# 上記の app.run_server(...) 行は削除するかコメントアウトしてください。
# Render環境では gunicorn が server オブジェクトを使って起動します。
