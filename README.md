# Jigsaw-puzzle solver
Synthesises jigsaw puzzle pieces from a given image. Contour detection and shape analysis used to characterise each piece and to reconstruct the original image by aligning compatible edges.

## Sheet music

### Original image and synthesised jigsaw puzzle pieces
<p>
  <span style="display:inline-block; width:49%; text-align:center; vertical-align:top;">
    <img src="sheet_music.jpg" alt="Sheet music original" width="45%"/>
  </span>
  <span style="display:inline-block; width:49%; text-align:center; vertical-align:top;">
    <img src="present/sheet_music_all_pieces_green.jpg" alt="Sheet music — Generated jigsaw puzzle pieces" width="52%"/>

  </span>
</p>


### Single piece processing (left to right)
<p>
  <span style="display:inline-block; width:24%; text-align:center;">
    <img src="present/p05.jpg" alt="jigsaw piece" width="20%"/>
    <br/>
    <sub>Jigsaw piece</sub>
  </span>
  <span style="display:inline-block; width:24%; text-align:center;">
    <img src="present/contour.jpg" alt="contour" width="20%"/>
    <br/>
    <sub>Contour</sub>
  </span>
  <span style="display:inline-block; width:24%; text-align:center;">
    <img src="present/green_removed.jpg" alt="background removal" width="20%"/>
    <br/>
    <sub>Background removal</sub>
  </span>
  <span style="display:inline-block; width:24%; text-align:center;">
    <img src="present/coloured_edges.jpg" alt="edge detection" width="20%"/>
    <br/>
    <sub>Edge detection</sub>
  </span>
</p>

### Solved
![Sheet music solved](present/sheet_music_solved.jpg)

## Examples

<p>
  <span style="display:inline-block; width:49%; text-align:center; vertical-align:top;">
    <img src="present/sheet_music_all_pieces_green.jpg" alt="Sheet music — Generated jigsaw puzzle pieces" width="100%"/>
    <br/>
    <sub>Sheet music — Generated jigsaw puzzle pieces</sub>
  </span>
  <span style="display:inline-block; width:49%; text-align:center; vertical-align:top;">
    <img src="present/sheet_music_solved.jpg" alt="Sheet music — Solved" width="100%"/>
    <br/>
    <sub>Sheet music — Solved</sub>
  </span>
</p>
<p>
  <span style="display:inline-block; width:49%; text-align:center; vertical-align:top;">
    <img src="present/ladybirds_all_pieces_green.jpg" alt="Ladybirds — Generated jigsaw puzzle pieces" width="100%"/>
    <br/>
    <sub>Ladybirds — Generated jigsaw puzzle pieces</sub>
  </span>
  <span style="display:inline-block; width:49%; text-align:center; vertical-align:top;">
    <img src="present/ladybirds_solved.jpg" alt="Ladybirds — Solved" width="100%"/>
    <br/>
    <sub>Ladybirds — Solved</sub>
  </span>
</p>
<p>
  <span style="display:inline-block; width:49%; text-align:center; vertical-align:top;">
    <img src="present/rose_all_pieces_green.jpg" alt="Rose — Generated jigsaw puzzle pieces" width="100%"/>
    <br/>
    <sub>Rose — Generated jigsaw puzzle pieces</sub>
  </span>
  <span style="display:inline-block; width:49%; text-align:center; vertical-align:top;">
    <img src="present/rose_solved.jpg" alt="Rose — Solved" width="100%"/>
    <br/>
    <sub>Rose — Solved</sub>
  </span>
</p>
