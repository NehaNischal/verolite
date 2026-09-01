import subprocess

for commit in ["457410b", "67928b1", "2e14780"]:
    try:
        data = subprocess.check_output(["git", "show", f"{commit}:images/surface/arco-7.jpg"])
        print(f"Commit {commit} has arco-7.jpg ({len(data)} bytes)")
    except Exception as e:
        print(f"Commit {commit} failed: {e}")
