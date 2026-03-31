import os, zipfile

def unpack_asice(input_path="original.asice", extract_dir="contents_of_asice"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(input_path) as z:
        z.extractall(extract_dir)
        original_order = z.namelist()

    with open(os.path.join(extract_dir, "original_file_order.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(original_order))

unpack_asice()