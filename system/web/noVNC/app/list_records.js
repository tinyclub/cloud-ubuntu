function list_records(theme) {
    var data = new Array();
    var record = VNC_record_data;
    var player = VNC_record_player;
    var record_dir = VNC_record_dir;
    var target = document.getElementById('VNC_records');

    data.push("<table>\n")

    data.push("<tr class='head'>\n");
    data.push("<th> No. </th>\n");
    data.push("<th> Play </th>\n");
    data.push("<th> Speedup </th>\n");
    data.push("<th> Down </th>\n");

    var i, head = record[0];
    for (i = 1; i < head.length; i++)
        data.push("<th>" + head[i] + "</th>\n");
    data.push("</tr>\n");

    var bg, row, j, play_url, down_url;
    for (i = 1; i < record.length; i++) {
        bg = "even";
        if (i % 2 === 0)
            bg = "odd";
        data.push("<tr class='" + bg + "'>\n");
        data.push("<td> " + i + " </td>\n");

        row = record[i];

        down_url = record_dir + "/" + row[0];
	if (theme) {
            data.push("<td><input type='radio' name='session' onclick='load(" + i + ");'></td>\n");
            data.push("<td><input type='radio' name='session' onclick='load(" + i + ", \".slice\");'></td>\n");
	} else {
            play_url = player + "?data=" + row[0];
            data.push("<td><a href='" + play_url + "'>&gt;</a></td>\n");
            play_url = player + "?data=" + row[0] + ".slice";
            data.push("<td><a href='" + play_url + "'>&gt;</a></td>\n");
	}
        data.push("<td><a href='" + down_url + "'>v</a></td>\n");

        for (j = 1; j < row.length; j++)
            data.push("<td>" + row[j] + "</td>\n");

        data.push("</tr>\n");
    }

    data.push("</table>")

    target.innerHTML = data.join('');
}


function draw_records() {
    list_records(1);
}
