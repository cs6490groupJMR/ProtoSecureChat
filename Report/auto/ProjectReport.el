(TeX-add-style-hook "ProjectReport"
 (lambda ()
    (LaTeX-add-bibliographies)
    (LaTeX-add-labels
     "wbp:beginDH"
     "wbp:beginNonceExchange")
    (TeX-add-symbols
     "ScaleIfNeeded"
     "origincludegraphics")
    (TeX-run-style-hooks
     "geometry"
     "columnsep=20pt"
     "right=.5in"
     "left=.5in"
     "bottom=.5in"
     "top=.5in"
     "amssymb"
     "parskip"
     "fouriernc"
     "amsmath"
     "graphicx"
     "multicol"
     ""
     "latex2e"
     "art10"
     "article"
     "twoside")))

