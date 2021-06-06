#!/bin/sh

git clone -b v3.0.4 https://github.com/attardi/wikiextractor.git /wikiextractor
cd /wikiextractor
cat <<EOF > a.patch
diff --git a/wikiextractor/extract.py b/wikiextractor/extract.py
index 5dd2a93..0d93675 100644
--- a/wikiextractor/extract.py
+++ b/wikiextractor/extract.py
@@ -823,7 +823,7 @@ class Extractor():
         self.recursion_exceeded_3_errs = 0  # parameter recursion
         self.template_title_errs = 0

-    def clean_text(self, text, mark_headers=False, expand_templates=False,
+    def clean_text(self, text, mark_headers=True, expand_templates=False,
                    escape_doc=True):
         """
         :param mark_headers: True to distinguish headers from paragraphs
EOF
patch -p1 < a.patch
pip install .

cd /app
python -m wikiextractor.WikiExtractor $WIKI_FILE
