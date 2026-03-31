import os, zipfile

def repack_asice(extract_dir="contents_of_asice", output_path="changed.asice"):
    order_file = os.path.join(extract_dir, "original_file_order.txt")
    if not os.path.exists(order_file):
        raise FileNotFoundError("Run unpack_asice.py first — original_file_order.txt is missing")

    with open(order_file, encoding="utf-8") as f:
        order = [line.strip() for line in f if line.strip()]

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in order:
            path = os.path.join(extract_dir, name)
            if name == "mimetype":
                with open(path, "rb") as f:
                    z.writestr(name, f.read(), compress_type=zipfile.ZIP_STORED)
            else:
                z.write(path, name)

repack_asice()