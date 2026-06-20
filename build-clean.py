import os, sys

# CSS (compressed, all features)
CSS = open('C:/Users/Ara/rain-website/css.txt').read() if os.path.exists('C:/Users/Ara/rain-website/css.txt') else None

# Build HTML dynamically instead of inline-string
html = []

# Read original working version
with open('C:/Users/Ara/rain-website/index-original.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Extract the working JS from original (before it got corrupted by series insertion)
js_start = orig.rfind('<script>')
js_end = orig.rfind('</script>')
working_js = orig[js_start+8:js_end]

# Build the clean file using the working JS as-is, but patch series content
# Strategy: strip everything between <style> and </script>, keep the rest
head = orig[:orig.find('<style>')]
tail_start = orig.rfind('</script>') + 9
tail = orig[tail_start:]

print(f"Head: {len(head)} chars")
print(f"JS: {len(working_js)} chars")
print(f"Tail: {len(tail)} chars")
print("Ready to build")
