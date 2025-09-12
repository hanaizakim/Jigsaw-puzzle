# Jigsaw-puzzle solver
Synthesises jigsaw puzzle pieces from a given image. Contour detection and shape analysis used to characterise each piece and to reconstruct the original image by aligning compatible edges.

## Sheet music

### Original image and synthesised jigsaw puzzle pieces
<p>
  <img src="sheet_music.jpg" alt="Sheet music original" width="45%"/>
  <img src="present/sheet_music_all_pieces_green.jpg" alt="Sheet music — all pieces (green)" width="52%"/>

</p>


### Single piece processing
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">

  <!-- Row of images -->
  <div style="display: flex; gap: 20px; justify-content: center;">
    <img src="present/p05.jpg" alt="jigsaw piece" style="width: 100px;"/>
    <img src="present/contour.jpg" alt="contour" style="width: 100px;"/>
    <img src="present/green_removed.jpg" alt="background removal" style="width: 100px;"/>
    <img src="present/coloured_edges.jpg" alt="edge detection" style="width: 100px;"/>
  </div>

  <!-- Row of labels -->
  <div style="display: flex; gap: 20px; justify-content: center;">
    <div>Jigsaw piece</div>
    <div>Contour</div>
    <div>Background removal</div>
    <div>Edge detection</div>
  </div>

</div>


### Solved
![Sheet music solved](present/sheet_music_solved.jpg)

## Examples

<p>
  <img src="present/sheet_music_all_pieces_green.jpg" alt="Sheet music — Generated jigsaw puzzle pieces" width="49%"/>
  <img src="present/sheet_music_solved.jpg" alt="Sheet music Solved" width="45%"/>
</p>
<p>
  <img src="present/ladybirds_all_pieces_green.jpg" alt="Ladybirds — Generated jigsaw puzzle pieces" width="49%"/>
  <img src="present/ladybirds_solved.jpg" alt="Ladybirds Solved" width="45%"/>
</p>
<p>
  <img src="present/rose_all_pieces_green.jpg" alt="Rose — Generated jigsaw puzzle pieces" width="49%"/>
  <img src="present/rose_solved.jpg" alt="Rose Solved" width="49%"/>
</p>
