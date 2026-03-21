#!/bin/bash
# 自動化帝国 ビルドスクリプト
# スプライト生成 → pyxel app2html → ゲームパッド無効化 → プレイログ送信JS注入 を自動で行う

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== 自動化帝国 ビルド ==="

# 1. スプライトシート生成（パッケージング前に実行、Pillow必須）
if [ -f build_sprites.py ]; then
    if python3 -c "from PIL import Image" 2>/dev/null; then
        echo "[1/5] スプライトシート生成..."
        python3 build_sprites.py
        echo "       → OK"
    else
        echo "[1/5] スキップ（Pillow未インストール。スプライト再生成が必要なら: pip install Pillow）"
    fi
else
    echo "[1/5] スキップ（build_sprites.py なし）"
fi

# 2. pyxapp をパッケージ（不要ファイルを一時退避して除外）
echo "[2/5] pyxapp パッケージング..."
mkdir -p /tmp/_build_backup
mv assets/originals /tmp/_build_backup/originals
[ -f automation-empire.pyxapp ] && mv automation-empire.pyxapp /tmp/_build_backup/
[ -f automation-empire.html ] && mv automation-empire.html /tmp/_build_backup/
[ -f .pyxignore ] && mv .pyxignore /tmp/_build_backup/
pyxel package . main.py
mv /tmp/_build_backup/originals assets/originals
rm -rf /tmp/_build_backup

# 3. HTML 生成
echo "[3/5] HTML 生成..."
pyxel app2html automation-empire.pyxapp

# 4. バーチャルゲームパッド無効化（app2html が毎回 enabled に戻すため）
echo "[4/5] バーチャルゲームパッド無効化..."
sed -i 's/gamepad: "enabled"/gamepad: "disabled"/' automation-empire.html

# 確認
if grep -q 'gamepad: "disabled"' automation-empire.html; then
    echo "       → OK: gamepad disabled"
else
    echo "       → WARNING: gamepad の置換に失敗した可能性あり"
    exit 1
fi

# 5. スマホ向けCSS/meta注入（タッチ座標ズレ対策 + カーソル非表示）
echo "[5/7] スマホ向けCSS/meta注入..."
MOBILE_HEAD='<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><style>canvas{touch-action:none;cursor:none;display:block;margin:0 auto;width:100vw;height:auto;max-height:100vh;max-width:100vh*270/480}body{margin:0;padding:0;overflow:hidden;background:#000}</style>'
# </head>の前に挿入（Pyxel HTMLに<head>がない場合は先頭に追加）
if grep -q '</head>' automation-empire.html; then
    sed -i "s|</head>|${MOBILE_HEAD}</head>|" automation-empire.html
else
    sed -i "1s|^|${MOBILE_HEAD}|" automation-empire.html
fi
echo "       → OK: mobile CSS/meta injected"

# 6. プレイログ送信JS注入（GAS エンドポイントが設定されていれば）
echo "[6/7] プレイログ送信JS注入..."
GAS_ENDPOINT_FILE="$SCRIPT_DIR/gas_endpoint.txt"
if [ -f "$GAS_ENDPOINT_FILE" ]; then
    GAS_URL=$(cat "$GAS_ENDPOINT_FILE" | tr -d '[:space:]')
    if [ "$GAS_URL" != "PLACEHOLDER" ] && [ -n "$GAS_URL" ]; then
        # console.logをフックして[PLAY_SUMMARY]をGASに送信するJSを注入
        ANALYTICS_JS="<script>(function(){var u=\"${GAS_URL}\";var o=console.log;console.log=function(){o.apply(console,arguments);var m=Array.prototype.join.call(arguments,\" \");if(m.indexOf(\"[PLAY_SUMMARY]\")===0){try{var d=JSON.parse(m.substring(14));d.session_id=Date.now().toString(36)+Math.random().toString(36).substr(2,5);d.user_agent=navigator.userAgent;fetch(u,{method:\"POST\",mode:\"no-cors\",headers:{\"Content-Type\":\"application/json\"},body:JSON.stringify(d)});}catch(e){o(\"[Analytics] Error:\",e);}}};})();</script>"
        # HTMLの末尾に追加
        echo "$ANALYTICS_JS" >> automation-empire.html
        echo "       → OK: analytics JS injected (GAS endpoint set)"
    else
        echo "       → スキップ（gas_endpoint.txt が PLACEHOLDER のまま）"
    fi
else
    echo "       → スキップ（gas_endpoint.txt なし）"
fi

echo ""
echo "=== ビルド完了 ==="
echo "automation-empire.html が更新されたよ。"
