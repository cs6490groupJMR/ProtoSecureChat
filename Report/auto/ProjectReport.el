(TeX-add-style-hook "ProjectReport"
 (lambda ()
    (LaTeX-add-bibliographies)
    (TeX-run-style-hooks
     "geometry"
     "columnsep=20pt"
     "right=1in"
     "left=1in"
     "bottom=1in"
     "top=1in"
     "amssymb"
     "parskip"
     "fouriernc"
     "amsmath"
     "multicol"
     ""
     "latex2e"
     "art10"
     "article"
     "twoside")))

