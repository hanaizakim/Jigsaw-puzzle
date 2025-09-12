# Jigsaw-puzzle solver
Synthesises jigsaw puzzle pieces from a given image. Contour detection and shape analysis used to characterise each piece and to reconstruct the original image by aligning compatible edges.

## Sheet music

### Original image and synthesised jigsaw puzzle pieces
<p>
  <img src="sheet_music.jpg" alt="Sheet music original" width="45%"/>
  <img src="present/sheet_music_all_pieces_green.jpg" alt="Sheet music — all pieces (green)" width="52%"/>

</p>


### Single piece processing
<table>
    <tr>
        <td><img src="present/p05.jpg" width="100"/></td>
        <td><img src="present/contour.jpg" width="100"/></td>
        <td><img src="present/green_removed.jpg" width="100"/></td>
        <td><img src="present/coloured_edges.jpg" width="100"/></td>
    </tr>
    <tr>
        <td align="center">Jigsaw piece</td>
        <td align="center">Piece contour</td>
        <td align="center">Background removal</td>
        <td align="center">Edge detection</td>
    </tr>
</table>



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
