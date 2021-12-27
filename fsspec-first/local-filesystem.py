import fsspec

fs = fsspec.filesystem('file')

BASE_DIR = "/tmp/output"

fs.mkdir(f"{BASE_DIR}", parents=True, exist_ok=True)
fs.touch(f"{BASE_DIR}/success")  # creates empty file
assert fs.exists(f"{BASE_DIR}/success")
assert fs.isfile(f"{BASE_DIR}/success")
assert fs.cat(f"{BASE_DIR}/success") == b""  # get content as bytestring
fs.copy(f"{BASE_DIR}/success", "/tmp/output/copy")

print(fs.ls(f"{BASE_DIR}", detail=False))

# absolute path를 반환한다.
assert fs.ls(f"{BASE_DIR}", detail=False) == [f"{BASE_DIR}/success", f"{BASE_DIR}/copy"]
fs.rm(f"{BASE_DIR}", recursive=True)
