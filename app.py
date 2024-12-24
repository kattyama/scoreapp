#ver1.0
import streamlit as st
import pandas as pd

st.set_page_config(initial_sidebar_state="expanded")

st.title("スコア差計算アプリ")

# サイドバー
st.sidebar.title("設定")
num_people = st.sidebar.number_input("人数", min_value=2, step=1, value=3)
num_games = st.sidebar.number_input("ゲーム数", min_value=1, step=1, value=2)
price_per_point = st.sidebar.number_input(
    "1ポイントあたりの金額", min_value=10, max_value=10000, step=10, value=100
)
st.write('---')
# プレイヤー名入力 (サイドバーに移動)
player_names = []
for i in range(num_people):
    player_names.append(st.sidebar.text_input(f"プレイヤー{i+1}の名前", f"プレイヤー{i+1}", key=f"player_name_{i}"))

# スコア入力
all_scores = []
for game in range(num_games):
    st.write(f"### 第{game+1}ゲーム")
    scores = {}
    for i in range(num_people):
        score = st.number_input(f"{player_names[i]}のスコア", value=0, key=f"score_{game}_{i}")
        scores[i] = score  # インデックスをキーとして使用
    all_scores.append(scores)

# 計算と表示
if len(all_scores) > 0 and len(all_scores[0]) > 1:
    all_game_data = []
    all_individual_profit_loss = {}
    all_player_transactions = {}

    # 初期化 (インデックスをキーとして使用)
    for i in range(num_people):
        all_individual_profit_loss[i] = {"損益額合計": 0, "スコア差合計値": 0}
        all_player_transactions[i] = []

    for game_index, scores in enumerate(all_scores):
        data = []
        for i in range(num_people):
            for j in range(num_people):
                if i != j:
                    score_diff = scores[j] - scores[i]
                    profit_loss = score_diff * price_per_point
                    data.append(
                        {
                            f"対戦(G{game_index+1})": f"{player_names[i]} vs {player_names[j]}", # プレイヤー名を使用
                            f"スコア差(G{game_index+1})": score_diff,
                            f"損益額(G{game_index+1})": profit_loss,
                        }
                    )
        all_game_data.append(data)
        df = pd.DataFrame(data)

        try:
            for index, row in df.iterrows():
                names_in_match = row[f"対戦(G{game_index+1})"].split(" vs ")
                i = player_names.index(names_in_match[0]) # プレイヤー名からインデックスを取得
                j = player_names.index(names_in_match[1]) # プレイヤー名からインデックスを取得
                score_diff = row[f"スコア差(G{game_index+1})"]
                profit_loss = row[f"損益額(G{game_index+1})"]

                all_individual_profit_loss[i]["損益額合計"] += profit_loss
                all_individual_profit_loss[i]["スコア差合計値"] += score_diff
                all_individual_profit_loss[j]["損益額合計"] -= profit_loss
                all_individual_profit_loss[j]["スコア差合計値"] -= score_diff

                # 取引情報の追加
                all_player_transactions[i].append({
                    "相手": player_names[j], # プレイヤー名を使用
                    "ゲーム": game_index + 1,
                    "スコア差": score_diff,
                    "収支": profit_loss
                })
        except KeyError as e:
            st.write(f"KeyErrorが発生しました: {e}")
            st.write(f"現在のDataFrameのカラム: {df.columns}")
            st.write(f"現在のDataFrame:\n{df}")
            st.stop()
    st.write('---')
    # スコア差と損益の表示
    st.write("### スコア差と損益")
    combined_df = pd.concat([pd.DataFrame(game_data) for game_data in all_game_data], axis=1)
    st.dataframe(combined_df)

    st.write('---')
    # 一人あたりの損益額の表示
    st.write("### 一人あたりの損益額")
    individual_profit_loss_data = []
    for i in range(num_people): # インデックスでループ
        individual_profit_loss_data.append({
            "プレイヤー": player_names[i], # プレイヤー名を表示
            "損益額合計": all_individual_profit_loss[i]["損益額合計"]/2,
            "スコア差合計値": all_individual_profit_loss[i]["スコア差合計値"]/2
        })

    columns = ["プレイヤー", "損益額合計", "スコア差合計値"]
    individual_profit_loss_df = pd.DataFrame(individual_profit_loss_data, columns=columns)
    st.dataframe(individual_profit_loss_df)

    # 各プレイヤーの収支表
    st.write("### 各プレイヤーの収支")
    for i in range(num_people):
        st.write(f"#### {player_names[i]}の収支")
        transactions_df = pd.DataFrame(all_player_transactions[i])
        st.dataframe(transactions_df)
    st.write('---')

else:
    st.write("2人以上のプレイヤーのスコアを入力してください。")


