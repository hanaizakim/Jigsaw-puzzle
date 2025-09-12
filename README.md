# Jigsaw-puzzle solver
Synthesises jigsaw puzzle pieces from a given image. Contour detection and shape analysis used to characterise each piece and to reconstruct the original image by aligning compatible edges.

## Sheet music

### Original image and all pieces (green)
<p>
  <img src="sheet_music.jpg" alt="Sheet music original" width="49%"/>
  <img src="present/sheet_music_all_pieces_green.jpg" alt="Sheet music — all pieces (green)" width="49%"/>

</p>


### Single piece processing (left to right)
<p>
  <span style="display:inline-block; width:24%; text-align:center;">
    <img src="present/p05.jpg" alt="jigsaw piece" width="100%"/>
    <br/>
    <sub>Jigsaw piece</sub>
  </span>
  <span style="display:inline-block; width:24%; text-align:center;">
    <img src="present/contour.jpg" alt="contour" width="100%"/>
    <br/>
    <sub>Contour</sub>
  </span>
  <span style="display:inline-block; width:24%; text-align:center;">
    <img src="present/green_removed.jpg" alt="background removal" width="100%"/>
    <br/>
    <sub>Background removal</sub>
  </span>
  <span style="display:inline-block; width:24%; text-align:center;">
    <img src="present/coloured_edges.jpg" alt="edge detection" width="100%"/>
    <br/>
    <sub>Edge detection</sub>
  </span>
</p>

### Solved
![Sheet music solved](present/sheet_music_solved.jpg)

## Examples

<p>
  <img src="present/sheet_music_all_pieces_green.jpg" alt="Sheet music — Generated jigsaw puzzle pieces" width="49%"/>
  <img src="present/sheet_music_solved.jpg" alt="Sheet music Solved" width="49%"/>
</p>
<p>
  <img src="present/ladybirds_all_pieces_green.jpg" alt="Ladybirds — Generated jigsaw puzzle pieces" width="49%"/>
  <img src="present/ladybirds_solved.jpg" alt="Ladybirds Solved" width="49%"/>
</p>
<p>
  <img src="present/rose_all_pieces_green.jpg" alt="Rose — Generated jigsaw puzzle pieces" width="49%"/>
  <img src="present/rose_solved.jpg" alt="Rose Solved" width="49%"/>
</p>
