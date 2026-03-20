#!/bin/bash
# 自動化帝国 ビルドスクリプト
# スプライト生成 → pyxel app2html → ゲームパッド無効化 を自動で行う

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== 自動化帝国 ビルド ==="

# 1. スプライトシート生成（パッケージング前に実行、Pillow必須）
if [ -f build_sprites.py ]; then
    if python3 -c "from PIL import Image" 2>/dev/null; then
        echo "[1/4] スプライトシート生成..."
        python3 build_sprites.py
        echo "       → OK"
    else
        echo "[1/4] スキップ（Pillow未インストール。スプライト再生成が必要なら: pip install Pillow）"
    fi
else
    echo "[1/4] スキップ（build_sprites.py なし）"
fi

# 2. pyxapp をパッケージ（不要ファイルを一時退避して除外）
echo "[2/4] pyxapp パッケージング..."
mkdir -p /tmp/_build_backup
mv assets/originals /tmp/_build_backup/originals
[ -f automation-empire.pyxapp ] && mv automation-empire.pyxapp /tmp/_build_backup/
[ -f automation-empire.html ] && mv automation-empire.html /tmp/_build_backup/
[ -f .pyxignore ] && mv .pyxignore /tmp/_build_backup/
pyxel package . main.py
mv /tmp/_build_backup/originals assets/originals
rm -rf /tmp/_build_backup

# 3. HTML 生成
echo "[3/4] HTML 生成..."
pyxel app2html automation-empire.pyxapp

# 4. バーチャルゲームパッド無効化（app2html が毎回 enabled に戻すため）
echo "[4/4] バーチャルゲームパッド無効化..."
sed -i 's/gamepad: "enabled"/gamepad: "disabled"/' automation-empire.html

# 確認
if grep -q 'gamepad: "disabled"' automation-empire.html; then
    echo "       → OK: gamepad disabled"
else
    echo "       → WARNING: gamepad の置換に失敗した可能性あり"
    exit 1
fi

echo ""
echo "=== ビルド完了 ==="
echo "automation-empire.html が更新されたよ。"
