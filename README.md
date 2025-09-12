# Jigsaw-puzzle solver
Synthesises jigsaw puzzle pieces from a given image. Contour detection and shape analysis used to characterise each piece and to reconstruct the original image by aligning compatible edges.

## Sheet music

### Original image and synthesised jigsaw puzzle pieces
<p>
  <img src="sheet_music.jpg" alt="Sheet music original" width="45%"/>
  <img src="present/sheet_music_all_pieces_green.jpg" alt="Sheet music — all pieces (green)" width="52%"/>

</p>


### Single piece processing
<div style="
  display: grid;
  grid-template-columns: repeat(4, 150px);
  grid-template-rows: 150px 150px;
  gap: 10px;
  justify-content: center;
  text-align: center;
">

  <img src="present/p05.jpg" alt="jigsaw piece" style="width: 100%; height: 100%; object-fit: contain;"/>
  <img src="present/contour.jpg" alt="contour" style="width: 100%; height: 100%; object-fit: contain;"/>
  <img src="present/green_removed.jpg" alt="background removal" style="width: 100%; height: 100%; object-fit: contain;"/>
  <img src="present/coloured_edges.jpg" alt="edge detection" style="width: 100%; height: 100%; object-fit: contain;"/>

  <div style="
    width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
    border: 1px solid #ccc; background: #f9f9f9; font-weight: 600;">
    Jigsaw piece
  </div>
  <div style="
    width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
    border: 1px solid #ccc; background: #f9f9f9; font-weight: 600;">
    Contour
  </div>
  <div style="
    width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
    border: 1px solid #ccc; background: #f9f9f9; font-weight: 600;">
    Background removal
  </div>
  <div style="
    width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
    border: 1px solid #ccc; background: #f9f9f9; font-weight: 600;">
    Edge detection
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
