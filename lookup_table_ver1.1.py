import streamlit as st
import pandas as pd
from PIL import Image
from sklearn.neighbors import NearestNeighbors
import base64

# 注意事項説明
st.title("Look up Table 更新App Ver.1.1")
st.write('<span style="color:red;background:pink">"インポートするCSVの注意点"</span>', unsafe_allow_html=True)
st.write("※ #VALUE!、#DIV/0! などが含まれているとエラー表示になります。")

img = Image.open("210908_エラー注意.png")
st.image(img, caption="CSVに関する注意事項", use_column_width=True)

# 何も操作をしていない状態（ファイルアップロードボタンが表示される）
uploaded_file = st.file_uploader("学習用のCSVファイルをアップロード", type={"csv", "txt"})
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

# ファイルをアップロードすると下記のコードが動き出す
if uploaded_file:
    # アップロードしたCSV
    dat_train = uploaded_df

    # アップロードしたCSVファイルを表示
    st.write("アップロードしたCSVファイル")
    dat_train
    # 学習用データの編集
    df_train = dat_train.loc[:, ["KH2", "SH1", "SO1", "JS2"] ]

    # 検証用のCSVファイルの読み込み
    dat_test = pd.read_csv("fake_values.csv")
    # 検証用データの編集
    df_test = dat_test.loc[:,["C(1)", "C(2)", "C(3)", "C(4)"]]
    # 検証用ファイルの表示
    st.write("検証用ファイル最初の5行を表示")
    st.table(df_test.head())

    # k近傍法 k5で実施
    nbrs1 = NearestNeighbors(n_neighbors=5, n_jobs=1).fit(df_train)
    distances1, indices1 = nbrs1.kneighbors(df_test)
      
    # dat_k5にDataFrame形式のdistances1をを代入
    dat_k5 = pd.DataFrame(data=distances1)
    # 検証データにk近傍法で計算したk5の列を結合(データ結合)
    sample_k5 = df_test.join([dat_k5[4]])
    # 列名を変更
    df_p = sample_k5.rename(columns={4: "K5"})
    # 完成したルックアップテーブルを表示
    st.write("完成したルックアップテーブルを表示")
    st.dataframe(df_p, width=1000, height=300)

    # 完成したCSVファイルのダウンロードリンク
    csv = df_p.to_csv(index=False)  
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="lookup_table.csv">download</a>'
    st.markdown(f"ダウンロードする {href}", unsafe_allow_html=True)