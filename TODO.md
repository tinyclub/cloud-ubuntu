
# noVNC

1. Allow to set 'record' and 'record file' via noVNC web ui.
2. Allow to download the 'record file'.
3. Allow to playback it immediately.
4. Add big data support: split to several small files and load separately
5. Add text/audio comment function for trackbar of the player
6. Don't reset while no real move.
7. Add timestamp info
8. Make sure the 1st frame is a full frame, not only part of a full screen (Check the size)?
9. Add speedup/slowdown feature? (not necessary, but available on the latest frame delay improve)
10. Connect Cloud-Lab automatically by allow select and launch the labs (random token and append to the token map).
11. Add audio play support: with <audio> meta
    * http://kolber.github.io/audiojs/
    * http://www.cnblogs.com/dragondean/p/jquery-audioplayer-js.html
    * https://msdn.microsoft.com/zh-cn/library/gg589529(v=vs.85).aspx
12. Add data compress with base64+lz4/decompress support for big data, python code...
    TODO: check the size diff between base64 and binary encoding
13. Add data compress support for splitted big data, python code...
14. Convert the records.html to a html page and a js data, allows to load and handle easierly
15. Clean up everything: include the variables, functions, js/css/html ...
16. Add big record list data splitting support, add sort and search support ...
