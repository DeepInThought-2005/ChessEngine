#!/bin/sh
# Build ChessL for the browser with pygbag (Pygame on WebAssembly).
# Usage: web/build.sh <output dir>   e.g. web/build.sh ../website/public/games
# Needs: pip install pygbag
set -eu
out=$(cd "$1" && pwd)
root=$(cd "$(dirname "$0")/.." && pwd)
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

# Only the code, images and sounds the game uses (no __pycache__).
mkdir -p "$stage/chessl/Image/Boards" "$stage/chessl/Image/Pieces" "$stage/chessl/Sound"
cp "$root"/ChessL/*.py "$stage/chessl/"
cp "$root/ChessL/Image/Boards/blue.png" "$stage/chessl/Image/Boards/"
cp -R "$root/ChessL/Image/Pieces/Staunty" "$stage/chessl/Image/Pieces/"
cp "$root"/ChessL/Sound/*.ogg "$stage/chessl/Sound/"

python -m pygbag --build --title chessl "$stage/chessl" >/dev/null
mkdir -p "$out/chessl"
web="$stage/chessl/build/web"
cp "$web/index.html" "$web/chessl.apk" "$web/chessl.tar.gz" "$web/favicon.png" "$out/chessl/"
# Let the game use the whole page instead of half its width.
sed -i.bak 's/gui_divider : 2,/gui_divider : 1,/' "$out/chessl/index.html" && rm "$out/chessl/index.html.bak"
echo "built $out/chessl"
