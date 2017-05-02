# 機械学習 - タイプ判定 - 
1. save_beautyful.pyでGoogleカスタム検索APIを使用して、タイプの画像とタイプでない画像をimages下に収集する
2. pickiup-faces.pyでiages下の画像を顔検出し、100x100にリサイズする
3. save_vector3.pyでfaces下の画像を三次元ベクトルに変換し、label(yes or no)と一緒に機械学習させ、pickleで学習ファイルを保存する
4. learn.pyでGoogle画像検索をimgタグのsrcをscraingし、タイプ判定器にかける