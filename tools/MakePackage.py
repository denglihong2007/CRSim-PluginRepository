import os
import zipfile
import shutil
import json
import yaml

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plugins_dir = os.path.join(base_dir, "plugins")
    icons_dir = os.path.join(base_dir, "icons")
    output_json = os.path.join(base_dir, "plugins.json")
    output_zip = os.path.join(base_dir, "output.zip")

    # 清理旧icons目录和json
    if os.path.exists(icons_dir):
        shutil.rmtree(icons_dir)
    os.makedirs(icons_dir, exist_ok=True)
    if os.path.exists(output_json):
        os.remove(output_json)
    if os.path.exists(output_zip):
        os.remove(output_zip)

    manifests = []
    for fname in os.listdir(plugins_dir):
        if fname.endswith(".crsp"):
            crsp_path = os.path.join(plugins_dir, fname)
            with zipfile.ZipFile(crsp_path, "r") as zf:
                # 读取manifest.yml
                with zf.open("manifest.yml") as mf:
                    manifest = yaml.safe_load(mf)
                    manifests.append(manifest)
                # 提取icon.png
                icon_name = os.path.splitext(fname)[0] + ".png"
                icon_out_path = os.path.join(icons_dir, icon_name)
                with zf.open("icon.png") as iconf, open(icon_out_path, "wb") as outf:
                    shutil.copyfileobj(iconf, outf)

    # 保存json
    with open(output_json, "w", encoding="utf-8") as jf:
        json.dump(manifests, jf, ensure_ascii=False, indent=2)

    # 打包output.zip
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        # plugins目录
        for root, _, files in os.walk(plugins_dir):
            for file in files:
                fpath = os.path.join(root, file)
                arcname = os.path.relpath(fpath, base_dir)
                zf.write(fpath, arcname)
        # icons目录
        for root, _, files in os.walk(icons_dir):
            for file in files:
                fpath = os.path.join(root, file)
                arcname = os.path.relpath(fpath, base_dir)
                zf.write(fpath, arcname)
        # plugins.json
        zf.write(output_json, os.path.basename(output_json))

    # 删除icons目录和json
    shutil.rmtree(icons_dir)
    os.remove(output_json)

if __name__ == "__main__":
    main()
