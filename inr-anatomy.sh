#!/usr/bin/env bash
# INR Anatomy Atlas: GitHub checkout, local Docker app and GitHub Pages.
set -euo pipefail
INSTALLER_VERSION="0.7.2"

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
REPO="${INR_GITHUB_REPO:-jeremylynch83/neurovascular-atlas}"
REPO_URL="${INR_REPO_URL:-https://github.com/${REPO}.git}"
CHECKOUT="${INR_CHECKOUT:-$HOME/Documents/GitHub/neurovascular-atlas}"
PORT="${PORT:-5173}"
CONTAINER="inr-anatomy-atlas"
ACTION="${1:-update}"
ZIP_ARG="${2:-}"
TEMP_DIR=""

die() { printf 'Error: %s\n' "$*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "Install $1, then run this command again."; }
cleanup() { [[ -z "$TEMP_DIR" ]] || rm -rf -- "$TEMP_DIR"; }
trap cleanup EXIT

usage() {
  cat <<'USAGE'
Usage: ./inr-anatomy.sh [update|local|publish|restart|status|stop|logs|help] [release.zip]

update   Clone/pull main, import a newer adjacent release ZIP, run locally,
         commit and push the app, and configure GitHub Pages (default).
local    Clone/pull and install locally without committing or publishing.
publish  Commit and publish the current checkout, without pulling or importing.
restart  Rebuild and restart the current checkout locally.
status   Show checkout, container, served version and Pages URL.
stop     Stop the local app.   logs: Follow container logs.

Default checkout: ~/Documents/GitHub/neurovascular-atlas
Local URL: http://localhost:5173
Keep this script and the latest inr-anatomy-atlas-v*.zip in the same folder.
GitHub authentication uses gh; the first run may open its browser login.
Overrides: INR_CHECKOUT, INR_GITHUB_REPO, PORT.
The previous ~/INR-Anatomy-Atlas installation and anatomy data are retained.
USAGE
}

version() {
  python3 - "$1/package.json" <<'PY'
import json,sys
print(json.load(open(sys.argv[1]))['version'])
PY
}

ensure_gh() {
  if ! command -v gh >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1; then
      printf 'Installing GitHub CLI (gh), needed for GitHub login and Pages.\n'
      sudo apt-get update
      sudo apt-get install -y gh
    else
      die 'Install GitHub CLI from https://cli.github.com/, then run again.'
    fi
  fi
  if ! gh auth status --hostname github.com >/dev/null 2>&1; then
    gh auth login --hostname github.com --git-protocol https --web --scopes workflow
  fi
  # Existing OAuth logins may lack permission to push workflow files.
  local headers scopes
  headers="$(gh api user --include)"
  scopes="$(printf '%s' "$headers" | python3 -c 'import re,sys; m=re.search(r"^x-oauth-scopes:[ \t]*([^\r\n]*)",sys.stdin.read(),re.I|re.M); print(m[1].replace(" ","") if m else "")')"
  if [[ -n "$scopes" && ",$scopes," != *',workflow,'* ]]; then
    gh auth refresh --hostname github.com --scopes workflow
  fi
  gh auth setup-git --hostname github.com
}

check_checkout() {
  [[ -d "$CHECKOUT/.git" || -f "$CHECKOUT/.git" ]] || die "$CHECKOUT is not a Git checkout."
  local origin
  origin="$(git -C "$CHECKOUT" remote get-url origin)"
  case "$origin" in
    "$REPO_URL"|"https://github.com/$REPO"|"git@github.com:$REPO.git"|"ssh://git@github.com/$REPO.git") ;;
    *) die "$CHECKOUT has a different origin: $origin" ;;
  esac
  [[ "$(git -C "$CHECKOUT" symbolic-ref --short HEAD)" == main ]] || die 'Switch the checkout to main before updating.'
}

check_clean() {
  [[ -z "$(git -C "$CHECKOUT" status --porcelain --untracked-files=normal)" ]] ||
    die "The checkout has uncommitted changes. Commit or move them before updating: $CHECKOUT"
}

prepare_checkout() {
  if [[ ! -e "$CHECKOUT" ]]; then
    mkdir -p -- "$(dirname "$CHECKOUT")"
    git clone "$REPO_URL" "$CHECKOUT"
    if ! git -C "$CHECKOUT" rev-parse --verify HEAD >/dev/null 2>&1; then
      git -C "$CHECKOUT" symbolic-ref HEAD refs/heads/main
    elif git -C "$CHECKOUT" show-ref --verify --quiet refs/remotes/origin/main; then
      git -C "$CHECKOUT" checkout main
    fi
  fi
  check_checkout
  check_clean
  git -C "$CHECKOUT" fetch origin
  if git -C "$CHECKOUT" show-ref --verify --quiet refs/remotes/origin/main; then
    git -C "$CHECKOUT" merge --ff-only origin/main
  fi
}

import_release() {
  # Extract safely and copy only application files. The Git history is retained.
  python3 - "$SCRIPT_DIR" "$CHECKOUT" "$ZIP_ARG" "$TEMP_DIR" <<'PY'
import json,os,re,shutil,stat,sys,zipfile,zlib
from pathlib import Path,PurePosixPath
source,dest,explicit,tmp=map(Path,(sys.argv[1],sys.argv[2],sys.argv[3] or '.',sys.argv[4]))
pattern=re.compile(r'inr-anatomy-atlas-v(\d+)\.(\d+)\.(\d+)\.zip$')
current=None
if (dest/'package.json').exists():
    current=json.loads((dest/'package.json').read_text())['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+',current):
        raise SystemExit('Error: checkout version must be a three-part release number.')
def key(p): return tuple(map(int,pattern.fullmatch(p.name).groups()))
if sys.argv[3]:
    archive=explicit.expanduser().resolve()
    if not archive.is_file(): raise SystemExit(f'Error: release ZIP not found: {archive}')
else:
    choices=[p for folder in {source,dest} for p in folder.glob('inr-anatomy-atlas-v*.zip') if pattern.fullmatch(p.name)]
    archive=max(choices,key=lambda p:(key(p),str(p))) if choices else None
if archive is None:
    if current is None: raise SystemExit('Error: empty repository. Place the app ZIP beside this script and run again.')
    print(f'Using Git checkout v{current}.'); raise SystemExit(0)
if not sys.argv[3] and current and key(archive)<=tuple(map(int,current.split('.'))):
    print(f'Using Git checkout v{current}; adjacent ZIP is not newer.'); raise SystemExit(0)
staging=tmp/'release'; staging.mkdir()
print(f'Checking release ZIP: {archive}',flush=True)
try:
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in info.filename or stat.S_ISLNK(info.external_attr>>16):
                raise SystemExit(f'Error: unsafe ZIP entry: {info.filename}')
            z.extract(info,staging)
except (zipfile.BadZipFile,EOFError,zlib.error) as error:
    raise SystemExit(
        f'Error: release ZIP is incomplete or corrupt: {archive}\n'
        'Replace it with a fresh download, wait for the download or Insync copy to finish, then run again.\n'
        'No release files were imported; the running app has not been changed.\n'
        f'Detail: {error}'
    ) from None
except (OSError,RuntimeError,NotImplementedError) as error:
    raise SystemExit(f'Error: cannot read release ZIP: {archive}\nDetail: {error}') from None
root=staging
if not (root/'package.json').is_file():
    children=[p for p in root.iterdir() if p.name!='__MACOSX']
    if len(children)==1 and children[0].is_dir(): root=children[0]
required=['package.json','package-lock.json','Dockerfile','docker.sh','anatomy.sh','build-anatomy.sh','src','public/anatomy','anatomy','tools','vite.config.ts']
if any(not (root/p).exists() for p in required): raise SystemExit('Error: ZIP is not a complete runnable app release.')
incoming=json.loads((root/'package.json').read_text())['version']
if not re.fullmatch(r'\d+\.\d+\.\d+',incoming): raise SystemExit('Error: invalid ZIP release version.')
if pattern.fullmatch(archive.name) and key(archive)!=tuple(map(int,incoming.split('.'))):
    raise SystemExit('Error: ZIP filename and package version disagree.')
if current and tuple(map(int,incoming.split('.')))<tuple(map(int,current.split('.'))):
    raise SystemExit(f'Error: refusing to downgrade {current} to {incoming}.')
# Replace owned trees so obsolete anatomy assets do not survive an upgrade.
# The preceding clean-checkout check protects local modifications.
for name in ['src','tools','anatomy','public/anatomy']:
    target=dest/name
    if target.is_symlink(): raise SystemExit(f'Error: application directory is a symlink: {target}')
    if target.exists(): shutil.rmtree(target)
paths=[]
for path in sorted(root.rglob('*')):
    rel=path.relative_to(root)
    if any(p in {'.git','node_modules','dist','.venv','anatomy-source','__MACOSX'} for p in rel.parts): continue
    if rel.parts[:2]==('docs','review') or path.name.endswith(('.zip','.tsbuildinfo')): continue
    target=dest/rel
    if path.is_dir(): target.mkdir(parents=True,exist_ok=True)
    elif path.is_file():
        if rel.as_posix()=='.gitignore' and target.exists(): continue
        # Never follow an existing checkout symlink while importing.
        if target.is_symlink() or any(p.is_symlink() for p in target.parents if p!=dest.parent):
            raise SystemExit(f'Error: refusing to write through a symlink: {target}')
        target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(path,target); paths.append(rel.as_posix())
(tmp/'imported-paths').write_bytes(b''.join(p.encode()+b'\0' for p in paths))
print(f'Installed v{incoming} in {dest}')
PY
  if [[ -f "$TEMP_DIR/imported-paths" ]]; then
    cp "$TEMP_DIR/imported-paths" "$(git -C "$CHECKOUT" rev-parse --absolute-git-dir)/inr-imported-paths"
  fi
}

install_integration() {
  [[ -f "$CHECKOUT/package.json" ]] || die 'No app found in the checkout.'
  chmod +x "$CHECKOUT/docker.sh" "$CHECKOUT/anatomy.sh" "$CHECKOUT/build-anatomy.sh"
  [[ ! -f "$CHECKOUT/inr-anatomy.sh" ]] || chmod +x "$CHECKOUT/inr-anatomy.sh"
  # An older permanent script must not downgrade a newer checkout's integration.
  if python3 - "$CHECKOUT/inr-anatomy.sh" "$INSTALLER_VERSION" <<'PY'
import re,sys
from pathlib import Path
p=Path(sys.argv[1]); text=p.read_text() if p.is_file() else ''
m=re.search(r'^INSTALLER_VERSION="(\d+\.\d+\.\d+)"',text,re.M)
sys.exit(0 if m and tuple(map(int,m[1].split('.')))>tuple(map(int,sys.argv[2].split('.'))) else 1)
PY
  then
    printf 'Keeping the newer installer and Pages workflow from the checkout.\n'
    return
  fi
  mkdir -p "$CHECKOUT/.github/workflows"
  cat > "$CHECKOUT/.github/workflows/pages.yml" <<'YAML'
name: Publish INR Anatomy Atlas
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: github-pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '22'
          cache: npm
      - id: pages
        uses: actions/configure-pages@v5
      - run: npm ci
      - run: npm run build
        env:
          INR_BASE: ${{ steps.pages.outputs.base_path }}/
      - uses: actions/upload-pages-artifact@v4
        with:
          path: dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
YAML
  if [[ "$SCRIPT_PATH" != "$(readlink -f "$CHECKOUT/inr-anatomy.sh")" ]]; then
    cp -- "$SCRIPT_PATH" "$CHECKOUT/inr-anatomy.sh"
  fi
  python3 - "$CHECKOUT/.gitignore" <<'PY'
import sys
from pathlib import Path
p=Path(sys.argv[1]); text=p.read_text() if p.exists() else ''
marker='# INR generated files'
if marker not in text:
    p.write_text(text.rstrip()+'\n\n'+marker+'\nnode_modules/\ndist/\n*.tsbuildinfo\n*.zip\n.venv/\nanatomy-source/\ndocs/review/\n')
PY
  chmod +x "$CHECKOUT/inr-anatomy.sh" "$CHECKOUT/docker.sh" "$CHECKOUT/anatomy.sh" "$CHECKOUT/build-anatomy.sh"
}

start_local() {
  need docker; need curl
  local expected previous actual=""
  expected="$(version "$CHECKOUT")"
  previous="$(docker inspect "$CONTAINER" --format '{{.Image}}' 2>/dev/null || true)"
  # docker.sh builds before replacing the running container.
  if ! PORT="$PORT" "$CHECKOUT/docker.sh" restart; then
    if [[ -n "$previous" && "$(docker inspect "$CONTAINER" --format '{{.Image}}' 2>/dev/null || true)" != "$previous" ]]; then
      docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
      docker run -d --rm --name "$CONTAINER" -p "$PORT:80" "$previous" >/dev/null ||
        die 'Docker startup failed and the previous image could not be restarted. Nothing was published.'
      printf 'Restored the previous local Docker image.\n' >&2
    fi
    die 'Docker build or startup failed. Nothing was published; inspect the output above, then retry ./inr-anatomy.sh publish.'
  fi
  for ((attempt=0; attempt<30; attempt++)); do
    actual="$(curl -fsS --connect-timeout 2 --max-time 3 "http://localhost:$PORT/anatomy/manifest.json" 2>/dev/null |
      python3 -c 'import json,sys; print(json.load(sys.stdin).get("release",""))' 2>/dev/null || true)"
    [[ "$actual" != "$expected" ]] || { printf 'Verified local app v%s at http://localhost:%s\n' "$actual" "$PORT"; return; }
    sleep 1
  done
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
  if [[ -n "$previous" ]]; then
    docker run -d --rm --name "$CONTAINER" -p "$PORT:80" "$previous" >/dev/null
    printf 'Restored the previous local Docker image.\n' >&2
  fi
  die "Expected v$expected on port $PORT, received '${actual:-no manifest}'. Nothing was published."
}

publish() {
  # Stage the app, never release ZIPs, authoring data, dependencies or build output.
  local imported
  imported="$(git -C "$CHECKOUT" rev-parse --absolute-git-dir)/inr-imported-paths"
  if [[ -f "$imported" ]]; then
    git -C "$CHECKOUT" add -f --pathspec-from-file="$imported" --pathspec-file-nul
  fi
  git -C "$CHECKOUT" add -A -- src tools anatomy public/anatomy
  for app_file in .dockerignore ATTRIBUTIONS.md CHANGELOG.md CREDITS.md Dockerfile LICENSE README.md THIRD_PARTY_ANATOMY.md anatomy.sh build-anatomy.sh docker.sh index.html nginx.conf package.json package-lock.json tsconfig.json vite.config.ts; do
    [[ ! -f "$CHECKOUT/$app_file" ]] || git -C "$CHECKOUT" add -f -- "$app_file"
  done
  git -C "$CHECKOUT" add -f -- .github/workflows/pages.yml .gitignore inr-anatomy.sh
  python3 - "$CHECKOUT" "$TEMP_DIR/assets" <<'PY'
import json,sys
from pathlib import Path,PurePosixPath
root=Path(sys.argv[1]); m=json.loads((root/'public/anatomy/manifest.json').read_text())
paths={'public/anatomy/manifest.json'}
for s in m['structures']:
    if not s.get('asset'): continue
    p=PurePosixPath(s['asset']['file'])
    if p.is_absolute() or '..' in p.parts: raise SystemExit('Error: unsafe manifest asset path.')
    paths.add('public/anatomy/'+str(p))
Path(sys.argv[2]).write_bytes(b''.join(p.encode()+b'\0' for p in sorted(paths)))
PY
  git -C "$CHECKOUT" add -f --pathspec-from-file="$TEMP_DIR/assets" --pathspec-file-nul
  if ! git -C "$CHECKOUT" diff --cached --quiet; then
    if ! git -C "$CHECKOUT" var GIT_AUTHOR_IDENT >/dev/null 2>&1; then
      local account login account_id name
      account="$(gh api user)"
      login="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["login"])' "$account")"
      account_id="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["id"])' "$account")"
      name="$(python3 -c 'import json,sys; d=json.loads(sys.argv[1]); print(d.get("name") or d["login"])' "$account")"
      git -C "$CHECKOUT" config user.name "$name"
      git -C "$CHECKOUT" config user.email "$account_id+$login@users.noreply.github.com"
    fi
    git -C "$CHECKOUT" commit -m "Update INR Anatomy Atlas to v$(version "$CHECKOUT") and publish Pages"
  fi
  if ! git -C "$CHECKOUT" push -u origin main; then
    die 'GitHub push failed. Local app is running. Check repository access; OAuth tokens need the workflow scope. Run gh auth refresh -h github.com -s workflow if needed, then ./inr-anatomy.sh publish.'
  fi
  rm -f -- "$imported"
  # Configure Pages after main exists, including newly created empty repositories.
  local settings build_type
  if settings="$(gh api "repos/$REPO/pages" 2>"$TEMP_DIR/pages-error")"; then
    build_type="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1]).get("build_type",""))' "$settings")"
    if [[ "$build_type" != workflow ]]; then
      printf '{"build_type":"workflow"}' | gh api -X PUT "repos/$REPO/pages" --input - >"$TEMP_DIR/pages-result" ||
        die 'The app was pushed, but Pages could not be switched to Actions. Check repository permissions, then run ./inr-anatomy.sh publish.'
    fi
  elif [[ "$(cat "$TEMP_DIR/pages-error")" == *'HTTP 404'* ]]; then
    printf '{"build_type":"workflow"}' | gh api -X POST "repos/$REPO/pages" --input - >"$TEMP_DIR/pages-result" ||
      die 'The app was pushed, but Pages could not be enabled. Check repository permissions and Pages availability, then run ./inr-anatomy.sh publish.'
  else
    cat "$TEMP_DIR/pages-error" >&2
    die 'The app was pushed, but Pages settings could not be read. Check GitHub access, then run ./inr-anatomy.sh publish.'
  fi
  # Dispatch also covers repeat publishing with no new commit and Pages just enabled.
  local dispatched=0
  for ((attempt=0; attempt<5; attempt++)); do
    if gh workflow run pages.yml --repo "$REPO" --ref main; then dispatched=1; break; fi
    sleep 2
  done
  if [[ "$dispatched" != 1 ]]; then
    die 'The app was pushed and Pages configured, but deployment could not be started. Check the Actions tab, then retry ./inr-anatomy.sh publish.'
  fi
  printf 'GitHub Pages deployment requested.\nPages: %s\nActions: https://github.com/%s/actions\n' \
    "$(gh api "repos/$REPO/pages" --jq .html_url)" "$REPO"
}

case "$ACTION" in
  help|-h|--help) usage; exit 0 ;;
  stop) need docker; docker rm -f "$CONTAINER" >/dev/null 2>&1 || true; printf 'Local app stopped.\n'; exit 0 ;;
  logs) need docker; exec docker logs -f "$CONTAINER" ;;
  status)
    printf 'Checkout: %s\n' "$CHECKOUT"
    if [[ -f "$CHECKOUT/package.json" ]]; then need python3; printf 'Checkout version: %s\n' "$(version "$CHECKOUT")"; fi
    if command -v git >/dev/null && [[ -e "$CHECKOUT/.git" ]]; then git -C "$CHECKOUT" status --short --branch; fi
    if command -v docker >/dev/null; then docker ps --filter "name=^/$CONTAINER$"; fi
    if command -v curl >/dev/null && command -v python3 >/dev/null; then
      curl -fsS --max-time 3 "http://localhost:$PORT/anatomy/manifest.json" | python3 -c 'import json,sys; print("Served version:",json.load(sys.stdin).get("release"))' || true
    fi
    printf 'Local: http://localhost:%s\nPages: https://%s.github.io/%s/\n' "$PORT" "${REPO%%/*}" "${REPO##*/}"
    if command -v tailscale >/dev/null; then ip="$(tailscale ip -4 2>/dev/null || true)"; [[ -z "$ip" ]] || printf 'Tailscale: http://%s:%s\n' "$ip" "$PORT"; fi
    exit 0 ;;
  update|local|publish|restart) ;;
  *) usage >&2; exit 2 ;;
esac
need git; need python3; need flock
mkdir -p -- "$(dirname "$CHECKOUT")"
exec 9>"${CHECKOUT}.update.lock"
flock -n 9 || die 'Another atlas update is already running.'
TEMP_DIR="$(mktemp -d)"
case "$ACTION" in
  update|local)
    need docker; need curl
    [[ "$ACTION" == local ]] || ensure_gh
    prepare_checkout
    import_release
    install_integration
    start_local
    if [[ "$ACTION" == update ]]; then publish; else printf 'Local changes are ready. Run ./inr-anatomy.sh publish to sync them to GitHub.\n'; fi ;;
  publish)
    ensure_gh; check_checkout
    git -C "$CHECKOUT" diff --cached --quiet || die 'Unstage existing changes before publishing; this command stages the app itself.'
    install_integration
    start_local
    publish ;;
  restart)
    check_checkout
    start_local ;;
esac
