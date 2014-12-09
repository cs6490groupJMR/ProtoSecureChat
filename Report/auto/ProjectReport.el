(TeX-add-style-hook "ProjectReport"
 (lambda ()
    (LaTeX-add-bibliographies)
    (LaTeX-add-environments
     "Figure")
    (LaTeX-add-labels
     "sec:protoDef"
     "wbp:beginDH"
     "wbp:beginNonceExchange"
     "fig:fullProto"
     "fig:basicProto"
     "fig:sslProto")
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
     "caption"
     "graphicx"
     "multicol"
     ""
     "latex2e"
     "art10"
     "article"
     "10pt"
     "twoside")))

